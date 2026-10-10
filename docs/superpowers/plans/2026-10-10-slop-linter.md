# Slop-Linter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `my-ai` 仓内实现独立的 slop-linter agent（双层：oxlint+anti-slop 机械层 / agent 语义层），需求开发完成后零侵入检测目标仓库的 AI-slop。

**Architecture:** `.agents/skills/slop-linter/` 真身目录 = SKILL.md（编排）+ semantic-rules.md（自然语言规则唯一源）+ engine/（自包含确定性核心：runner.sh + oxlint + vendored anti-slop + slop-local 自定义插件）。harness-kit 仅加一行文档提醒。

**Tech Stack:** bash + git + jq（runner/selfcheck）；oxlint + @oxlint/plugins（精确同版本 pin）+ vendored dmmulroy/anti-slop（ESLint v9 兼容 JS 插件，jiti 加载 TS）。

**Spec:** `docs/superpowers/specs/2026-10-10-slop-linter-design.md`（本计划从 spec 立论，执行者须同时读 spec）

## Global Constraints（每个任务隐含遵守）

- **目标仓库零侵入**：engine 对目标仓库只读；唯一写操作是修复循环且须用户显式确认（spec §2/§10）。
- **检测失效显式失败，绝不静默降级**（spec §11）。
- oxlint 与 @oxlint/plugins **同版本精确 pin**（spec §5.2）。
- `engine/node_modules/` 与 `engine/package-lock.json` 不入库（engine/.gitignore）。
- vendored `engine/anti-slop/` **不修改**（纪律）；个人 JS 规则只进 `engine/rules/`（spec §12.1）。
- 自然语言规则只写 `semantic-rules.md` 单一源；SKILL.md 零规则内容（spec §7）。
- Effect 规则组不启用（spec §5.3）。
- 本仓（my-ai）改动**直接本地 commit、不 push**（用户既有约定）；提交信息用 conventional commits。
- Bash 工具发出的命令不得含 `//` 或 `\\`（本环境 UNC 拦截）；文件内容不受限。npm/gh 命令用 `zsh -ic` 包装（token 在 ~/.zshrc）。
- 第三方 vendored 代码用 shell cp 拷贝（非 AI 创作，无归因问题）；我们自己的文件一律用 Write/Edit 工具。

## File Structure（本计划锁定）

```
.agents/skills/slop-linter/
├── SKILL.md                      # Task 5：编排层（两种调用模式 + Order + verdict + 修复循环）
├── README.md                     # Task 6：边界契约 + vendored 更新流程 + 推广
├── semantic-rules.md             # Task 4：SR 规则库种子
└── engine/
    ├── .gitignore                # Task 1：node_modules/ + package-lock.json
    ├── package.json              # Task 1：精确 pin（版本号 Task 1 解析）
    ├── oxlintrc.json             # Task 1 建（仅 anti-slop），Task 3 扩（slop-local）
    ├── runner.sh                 # Task 2：确定性入口
    ├── selfcheck.sh              # Task 2 建，Task 3 扩断言
    ├── anti-slop/                # Task 1：vendored src/ + LICENSE + VENDORED.md
    ├── rules/
    │   ├── index.ts              # Task 3：slop-local 插件入口
    │   └── rules/no-emoji.ts     # Task 3：首条自定义规则
    └── fixtures/
        ├── sloppy.ts             # Task 2：已知违规样本（Task 3 加 emoji 行）
        ├── sloppy.vue            # Task 2：.vue 覆盖性样本
        └── clean.ts              # Task 2：零违规样本
docs/superpowers/specs/2026-10-10-slop-linter-design.md   # Task 1 回写 spike 结论
harness-kit/skills/harness-dev/SKILL.md                   # Task 7：§8 加一行提醒
```

**已核实的环境事实**（执行者无需重查）：`my-ai/.agents/skills/` 是本工作区技能注册面，真身直放的目录（drawio-roadmap 等）会被 Qoder 自动发现为可调用技能，无需注册步骤；`~/.agents` 用户级非 git 仓（本期不用）。

---

### Task 1: Engine 脚手架 + vendored anti-slop + oxc JS 插件四项 spike

**Files:**
- Create: `.agents/skills/slop-linter/engine/package.json`
- Create: `.agents/skills/slop-linter/engine/.gitignore`
- Create: `.agents/skills/slop-linter/engine/oxlintrc.json`
- Create: `.agents/skills/slop-linter/engine/anti-slop/`（vendored 拷贝）
- Create: `/tmp/slop-spike/`（throwaway spike 样本，不入库）
- Modify: `docs/superpowers/specs/2026-10-10-slop-linter-design.md`（§13 spike 表回写结论）

**Interfaces:**
- Produces: 可执行的 `engine/node_modules/.bin/oxlint`；注册了 anti-slop 插件的 `engine/oxlintrc.json`（Task 2/3 直接引用）；spec §13 表的实测结论（Task 2 的 JSON 解析与 .vue 断言依据）。
- 本任务不产 runner；spike 直接手工调 oxlint。

- [ ] **Step 1: 解析要 pin 的版本号**

```bash
zsh -ic 'gh repo clone dmmulroy/anti-slop /tmp/anti-slop-src'
zsh -ic 'jq .devDependencies /tmp/anti-slop-src/package.json'
```

优先采用 anti-slop 自身 devDependencies 声明的 oxlint / @oxlint/plugins 版本对（它就是被这套版本验证过的）。若其中只有 oxlint 没有 @oxlint/plugins，再补查：

```bash
zsh -ic 'npm view @oxlint/plugins version'
```

把两个版本号记下来（下称 `<V>`，两包相同）。

- [ ] **Step 2: 建 engine 骨架并安装依赖**

用 Write 工具创建 `.agents/skills/slop-linter/engine/package.json`：

```json
{
  "name": "slop-linter-engine",
  "private": true,
  "version": "1.0.0",
  "description": "Deterministic mechanical layer of slop-linter (oxlint + anti-slop + slop-local)",
  "devDependencies": {
    "oxlint": "<V>",
    "@oxlint/plugins": "<V>"
  }
}
```

用 Write 工具创建 `.agents/skills/slop-linter/engine/.gitignore`：

```
node_modules/
package-lock.json
```

安装（限速网络，可能数分钟，Bash timeout 设 600000）：

```bash
zsh -ic 'cd /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine && npm install'
ls /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/node_modules/.bin/oxlint
```

Expected: oxlint 二进制存在。

- [ ] **Step 3: vendor anti-slop src/ 并记录 provenance**

```bash
mkdir -p /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine
cp -R /tmp/anti-slop-src/src /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/anti-slop
cp /tmp/anti-slop-src/LICENSE /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/anti-slop/LICENSE
zsh -ic 'git -C /tmp/anti-slop-src rev-parse HEAD'
```

用 Write 工具创建 `.agents/skills/slop-linter/engine/anti-slop/VENDORED.md`（把 `<REV>` 换成上一步输出）：

```markdown
# Vendored from dmmulroy/anti-slop

- upstream: https://github.com/dmmulroy/anti-slop
- revision: <REV>
- copied: src/ → ./ (含 vendor/eslint-stylistic 及其 LICENSE/UPSTREAM.md，MIT)
- date: 2026-10-10
- 本目录纪律：不修改（个人规则一律进 ../rules/）；升级走 slop-linter README 的更新流程
```

- [ ] **Step 4: 写初始 oxlintrc.json（仅 anti-slop）**

用 Write 工具创建 `.agents/skills/slop-linter/engine/oxlintrc.json`：

```json
{
  "jsPlugins": [
    { "name": "anti-slop", "specifier": "./anti-slop/index.ts" }
  ],
  "ignorePatterns": [
    ".agent/**", ".agents/**", ".claude/**", ".codex/**", ".cursor/**", ".gemini/**"
  ],
  "rules": {
    "oxc/no-accumulating-spread": "error",
    "anti-slop/no-array-filter-map": "error",
    "anti-slop/no-reduce-accumulator-copy": "error",
    "anti-slop/no-chained-type-assertions": "error",
    "anti-slop/no-conditional-empty-object-spread": "error",
    "anti-slop/no-known-value-widening": "error",
    "anti-slop/no-module-mocking": "error",
    "anti-slop/no-object-parameters": "error",
    "anti-slop/no-reflect-apply": "error",
    "anti-slop/no-reflect-get": "error",
    "anti-slop/no-runtime-typeof": "error",
    "anti-slop/no-shape-in-symbol-names": "error",
    "anti-slop/no-unknown-parameters": "error",
    "anti-slop/no-unknown-returns": "error",
    "anti-slop/no-unknown-type-aliases": "error",
    "anti-slop/no-unsafe-dictionary-type": "error",
    "anti-slop/no-widen-then-assert": "error",
    "anti-slop/require-readable-spacing": "error",
    "anti-slop/require-safety-comment-for-type-assertion": "error"
  }
}
```

- [ ] **Step 5: Spike 样本与四项验证**

用 Write 工具创建 `/tmp/slop-spike/sloppy.ts`：

```ts
interface User { id: string; email: string; active: boolean }
export type UserId = string;

export function sloppy(users: User[]): string[] {
  return users.filter((u) => u.active).map((u) => u.email);
}
export function widen(input: object): User {
  const user = input as object as User;
  return user;
}
export function runtimeCheck(input: unknown): string {
  if (typeof input === "string") { return input; }
  return "";
}
export function unsafeDict(value: string): UserId {
  const userId = value as UserId;
  return userId;
}
```

用 Write 工具创建 `/tmp/slop-spike/sloppy.vue`：

```vue
<script setup lang="ts">
declare const input: unknown;
export const label = typeof input === "string" ? input : "";
</script>
<template><div>{{ label }}</div></template>
```

逐项验证（cwd 必须在 /tmp/slop-spike，避免拾取 engine 目录配置）：

```bash
cd /tmp/slop-spike
ENG=/Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine
"$ENG/node_modules/.bin/oxlint" --config "$ENG/oxlintrc.json" --disable-nested-config -f json sloppy.ts
```

- **验证①（TS 插件从 json 配置加载）**：输出是 JSON 且包含 `anti-slop/no-array-filter-map`、`anti-slop/no-chained-type-assertions`、`anti-slop/no-runtime-typeof`、`anti-slop/require-safety-comment-for-type-assertion` 等 code。失败（报插件加载错误）→ 降级：把 oxlintrc.json 换成 `oxlint.config.ts`（`import { defineConfig } from "oxlint"` 形态，内容同上），并记入 spec §13。
- **验证②（-f json 结构）**：记录诊断对象的真实字段名（假定 `code` / `severity` / `message` / `location.start.line`；以实际为准，Task 2 的 jq 提取路径按此调整）。同时确认零违规时输出形如 `[]` 还是空串。
- **验证③（.vue script 块覆盖）**：

```bash
"$ENG/node_modules/.bin/oxlint" --config "$ENG/oxlintrc.json" --disable-nested-config -f json sloppy.vue
```

若 `anti-slop/no-runtime-typeof` 在 .vue 内触发 → jsPlugins 覆盖 .vue；否则不覆盖（Task 2 的 .vue 断言走"不覆盖"分支，spec §6 的兜底生效）。
- **验证④（--disable-nested-config + 显式 -c）**：

```bash
printf '{"rules":{"anti-slop/no-runtime-typeof":"off"}}' > .oxlintrc.json
"$ENG/node_modules/.bin/oxlint" --config "$ENG/oxlintrc.json" --disable-nested-config -f json sloppy.ts | jq '[.[] | select(.code == "anti-slop/no-runtime-typeof")] | length'
rm .oxlintrc.json
```

Expected: `1`（本地 off 配置未生效，kit 配置完全接管）。若为 `0` → nested config 泄漏，降级方案：runner 只传显式文件列表并再验证一次（记录到 spec §13）。

- [ ] **Step 6: 回写 spec §13 spike 表**

用 Edit 工具把 spec `docs/superpowers/specs/2026-10-10-slop-linter-design.md` §13 的表格四行改为实测结论（每行加"实测：<结论>"，失败的写明采用了哪条降级路径），并在 §13 末尾追加一行记录 JSON 诊断的真实字段名。

- [ ] **Step 7: Commit**

```bash
git add .agents/skills/slop-linter/engine docs/superpowers/specs/2026-10-10-slop-linter-design.md
git commit -m "feat(slop-linter): scaffold engine, vendor anti-slop, verify oxc js-plugin feasibility"
```

（`engine/anti-slop/` 是 cp 拷入的第三方代码，属 vendored 性质，随本任务入库；node_modules 已被 ignore。）

---

### Task 2: runner.sh（确定性入口）+ fixtures + selfcheck

**Files:**
- Create: `.agents/skills/slop-linter/engine/runner.sh`（`chmod +x`）
- Create: `.agents/skills/slop-linter/engine/selfcheck.sh`（`chmod +x`）
- Create: `.agents/skills/slop-linter/engine/fixtures/sloppy.ts`
- Create: `.agents/skills/slop-linter/engine/fixtures/sloppy.vue`
- Create: `.agents/skills/slop-linter/engine/fixtures/clean.ts`

**Interfaces:**
- Consumes: Task 1 的 `engine/oxlintrc.json`、`engine/node_modules/.bin/oxlint`；spec §13 已回写的 JSON 字段结论（下方代码按假定字段写，Step 3 按实测对齐）。
- Produces: `runner.sh --repo <path> [--base <ref>] [--files <p1,p2>] [--out <file>]` → JSON `{repo, base, head, dirty, nothingToLint, files:[{path, changedLines:[[s,e],…]}], diagnostics:[…], oxlintExitCode}`，exit 0/1/2（SKILL.md 与 selfcheck 依赖此契约）；`selfcheck.sh`（Task 3、以及今后每次规则调整/插件升级后必跑）。

- [ ] **Step 1: 写 fixtures（测试先行）**

用 Write 工具创建 `fixtures/sloppy.ts`（与 Task 1 spike 样本同内容，作为常驻断言样本）：

```ts
interface User { id: string; email: string; active: boolean }
export type UserId = string;

export function sloppy(users: User[]): string[] {
  return users.filter((u) => u.active).map((u) => u.email);
}
export function widen(input: object): User {
  const user = input as object as User;
  return user;
}
export function runtimeCheck(input: unknown): string {
  if (typeof input === "string") { return input; }
  return "";
}
export function unsafeDict(value: string): UserId {
  const userId = value as UserId;
  return userId;
}
```

`fixtures/sloppy.vue`（同 Task 1 spike 样本）；`fixtures/clean.ts`：

```ts
export const one = 1;
export function add(a: number, b: number): number {
  return a + b;
}
```

- [ ] **Step 2: 写 selfcheck.sh（此刻必然失败——runner 还不存在）**

用 Write 工具创建 `engine/selfcheck.sh`：

```bash
#!/usr/bin/env bash
# slop-linter selfcheck — fixtures 断言 + runner 端到端（spec §15）
set -uo pipefail
ENGINE_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
OXLINT="$ENGINE_DIR/node_modules/.bin/oxlint"
CFG="$ENGINE_DIR/oxlintrc.json"
FAIL=0
ok()   { echo "  ok  - $1"; }
miss() { echo "  FAIL- $1"; FAIL=1; }

echo "== part 1: rule engine on fixtures =="
OUT="$("$OXLINT" --config "$CFG" --disable-nested-config -f json "$ENGINE_DIR/fixtures/sloppy.ts")"
for rule in anti-slop/no-array-filter-map anti-slop/no-chained-type-assertions \
            anti-slop/no-runtime-typeof anti-slop/require-safety-comment-for-type-assertion; do
  if printf '%s' "$OUT" | jq -e --arg r "$rule" 'any(.[]; .code == $r)' >/dev/null; then
    ok "$rule fires"
  else
    miss "$rule does NOT fire (tune fixture until deterministic)"
  fi
done
CLEAN="$("$OXLINT" --config "$CFG" --disable-nested-config -f json "$ENGINE_DIR/fixtures/clean.ts")"
if printf '%s' "$CLEAN" | jq -e 'length == 0' >/dev/null; then ok "clean.ts zero findings"; else miss "clean.ts has findings"; fi

VUE_OUT="$("$OXLINT" --config "$CFG" --disable-nested-config -f json "$ENGINE_DIR/fixtures/sloppy.vue")"
# 按 Task 1 spec §13 实测结论二选一（执行时删掉不适用的分支）：
if printf '%s' "$VUE_OUT" | jq -e --arg r "anti-slop/no-runtime-typeof" 'any(.[]; .code == $r)' >/dev/null; then
  ok "jsPlugins covers .vue script blocks"
else
  echo "  note- jsPlugins does NOT cover .vue (spec §6 fallback active: native rules + semantic layer)"
fi

echo "== part 2: runner end-to-end (temp git repo) =="
TMP="$(mktemp -d)"
git init -q -b main "$TMP"
git -C "$TMP" config user.email t@t.local
git -C "$TMP" config user.name t
printf 'export const one = 1;\n' > "$TMP/a.ts"
git -C "$TMP" add a.ts
git -C "$TMP" commit -qm base
printf 'export const one = 1;\nexport const two = 2;\nexport const three = 3;\n' > "$TMP/a.ts"
git -C "$TMP" commit -qam change
JSON="$(bash "$ENGINE_DIR/runner.sh" --repo "$TMP" --base HEAD~1)"
if printf '%s' "$JSON" | jq -e '.files[0].path == "a.ts" and .files[0].changedLines == [[2,3]]' >/dev/null; then
  ok "runner changedLines = [[2,3]]"
else
  miss "runner changedLines wrong: $(printf '%s' "$JSON" | jq -c '.files')"
fi
if printf '%s' "$JSON" | jq -e '.diagnostics | length >= 1' >/dev/null; then
  ok "runner surfaces diagnostics for changed file"
else
  miss "runner diagnostics empty (expected findings for a.ts)"
fi
EMPTY="$(bash "$ENGINE_DIR/runner.sh" --repo "$TMP" --base HEAD)"
if printf '%s' "$EMPTY" | jq -e '.nothingToLint == true' >/dev/null; then
  ok "runner nothingToLint on empty diff"
else
  miss "runner empty-diff handling wrong"
fi
rm -rf "$TMP"

echo "== result =="
if [[ "$FAIL" -eq 0 ]]; then echo "selfcheck PASS"; else echo "selfcheck FAIL"; fi
exit "$FAIL"
```

（`.nothingToLint` 那条：`--base HEAD` 即 diff HEAD...HEAD 为空。注意 `a.ts` 含 `export` 三行在 no-unknown-returns 等规则下是否产 findings 未定，所以诊断断言用 `>= 1` 只验管道通；若实测为 0，把该断言改为 `has key .diagnostics` 存在性检查。）

- [ ] **Step 3: 跑 selfcheck 确认当前失败**

```bash
bash /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/selfcheck.sh
```

Expected: FAIL（`runner.sh: No such file or directory` / JSON 为空）。

- [ ] **Step 4: 实现 runner.sh**

用 Write 工具创建 `engine/runner.sh`：

```bash
#!/usr/bin/env bash
# slop-linter engine — deterministic mechanical layer (spec §5.1)
# Usage: runner.sh --repo <path> [--base <ref>] [--files <p1,p2>] [--out <file>]
# Exit: 0 = clean or nothing-to-lint · 1 = error-tier findings · 2 = usage/setup failure
set -euo pipefail

ENGINE_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
OXLINT_BIN="$ENGINE_DIR/node_modules/.bin/oxlint"
CONFIG="$ENGINE_DIR/oxlintrc.json"
die() { echo "runner: $*" >&2; exit 2; }

REPO="" BASE="" OUT="" FILES=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)  REPO="$2"; shift 2 ;;
    --base)  BASE="$2"; shift 2 ;;
    --files) FILES="$2"; shift 2 ;;
    --out)   OUT="$2"; shift 2 ;;
    *) die "unknown argument: $1" ;;
  esac
done
if [[ -z "$REPO" ]]; then die "--repo is required"; fi
if [[ ! -d "$REPO" ]]; then die "repo not found: $REPO"; fi
if [[ ! -f "$CONFIG" ]]; then die "config missing: $CONFIG"; fi
if [[ ! -x "$OXLINT_BIN" ]]; then die "oxlint not installed — run once: cd $ENGINE_DIR && npm install"; fi
REPO="$(cd "$REPO" && pwd)"

if [[ -z "$BASE" ]]; then
  DEFAULT="$(git -C "$REPO" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || true)"
  DEFAULT="${DEFAULT#origin/}"
  if [[ -z "$DEFAULT" ]]; then
    for c in main master; do
      if git -C "$REPO" show-ref --verify --quiet "refs/remotes/origin/$c"; then DEFAULT="$c"; break; fi
    done
  fi
  if [[ -z "$DEFAULT" ]]; then die "cannot resolve default branch — pass --base explicitly"; fi
  BASE="origin/$DEFAULT"
fi

DIRTY=false
if [[ -n "$(git -C "$REPO" status --porcelain)" ]]; then DIRTY=true; fi

# changed file set
if [[ -n "$FILES" ]]; then
  mapfile -t FILE_ARR < <(printf '%s\n' "$FILES" | tr ',' '\n' | grep -v '^$' || true)
else
  mapfile -t FILE_ARR < <(git -C "$REPO" diff --name-only "$BASE"...HEAD | grep -E '\.(ts|tsx|js|mjs|cjs|jsx|vue)$' || true)
fi

# changed line ranges per file (diff mode only)
declare -A RANGES=()
if [[ -z "$FILES" && ${#FILE_ARR[@]} -gt 0 ]]; then
  file="" ranges=""
  while IFS= read -r line; do
    if [[ "$line" == "+++ b/"* ]]; then
      if [[ -n "$file" ]]; then RANGES["$file"]="$ranges"; fi
      file="${line#+++ b/}"; ranges=""
    elif [[ "$line" == "@@"* ]]; then
      plus="${line#*+}"; plus="${plus%% *}"
      start="${plus%%,*}"
      if [[ "$plus" == *,* ]]; then count="${plus#*,}"; else count=1; fi
      if [[ "$count" -eq 0 ]]; then continue; fi
      ranges+="${start}-$((start + count - 1));"
    fi
  done < <(git -C "$REPO" diff --unified=0 "$BASE"...HEAD)
  if [[ -n "$file" ]]; then RANGES["$file"]="$ranges"; fi
fi

emit() {
  if [[ -n "$OUT" ]]; then printf '%s\n' "$1" > "$OUT"; else printf '%s\n' "$1"; fi
}

# nothing to lint: MUST skip oxlint (zero paths would lint the whole cwd)
if [[ ${#FILE_ARR[@]} -eq 0 ]]; then
  emit "$(jq -nc --arg repo "$REPO" --arg base "$BASE" --arg head "$(git -C "$REPO" rev-parse --short HEAD)" \
    --argjson dirty "$DIRTY" \
    '{repo:$repo, base:$base, head:$head, dirty:$dirty, nothingToLint:true, files:[], diagnostics:[], oxlintExitCode:0}')"
  exit 0
fi

FILES_JSON="[]"
for f in "${FILE_ARR[@]}"; do
  r="${RANGES[$f]:-}"
  FILES_JSON="$(printf '%s' "$FILES_JSON" | jq -c --arg p "$f" --arg r "$r" \
    '. + [{path: $p, changedLines: (if $r == "" then [] else ($r | rtrimstr(";") | split(";") | map(split("-") | map(tonumber))) end)}]')"
done

set +e
OXLINT_OUT="$(cd "$REPO" && "$OXLINT_BIN" --config "$CONFIG" --disable-nested-config -f json "${FILE_ARR[@]}")"
OXLINT_RC=$?
set -e
if [[ -z "$OXLINT_OUT" ]]; then OXLINT_OUT="[]"; fi
DIAG="$(printf '%s' "$OXLINT_OUT" | jq -c '.' 2>/dev/null)"
if [[ -z "$DIAG" ]]; then die "oxlint output is not valid JSON — report explicitly, never silently skip (spec §11)"; fi
ERRORS="$(printf '%s' "$DIAG" | jq '[.[] | select(.severity == "error")] | length')"

emit "$(jq -nc --arg repo "$REPO" --arg base "$BASE" --arg head "$(git -C "$REPO" rev-parse --short HEAD)" \
  --argjson dirty "$DIRTY" --argjson files "$FILES_JSON" --argjson diag "$DIAG" --argjson rc "$OXLINT_RC" \
  '{repo:$repo, base:$base, head:$head, dirty:$dirty, nothingToLint:false, files:$files, diagnostics:$diag, oxlintExitCode:$rc}')"

if [[ "$ERRORS" -gt 0 ]]; then exit 1; else exit 0; fi
```

```bash
chmod +x /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/runner.sh /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/selfcheck.sh
```

**实现说明（why，写给执行者）**：`set -e` 下所有 `[[ cond ]] && cmd` 短路写法都会在条件为假时误杀脚本，因此全部展开为 `if/fi`；`nothingToLint` 必须先于 oxlint 判断——oxlint 无路径参数时会 lint 整个 cwd，这是零侵入红线的反向事故；severity 字段名与取值按 Task 1 spec §13 回写的实测结论对齐（如实际是 `1/2` 数字或 `"warning"`，改 `select(.severity == "error")` 一处即可）。

- [ ] **Step 5: 跑 selfcheck 确认全绿**

```bash
bash /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/selfcheck.sh
```

Expected: `selfcheck PASS`（part1 四条 anti-slop 规则命中 + clean 零发现 + .vue 结论分支 + part2 三条 runner 断言）。任一 FAIL → 修 runner/fixture 至绿；fixture 允许为"确定命中"微调（fixture 服务于断言），runner 逻辑不许为绿灯改坏。

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/slop-linter/engine
git commit -m "feat(slop-linter): add deterministic runner with changed-line extraction and selfcheck"
```

---

### Task 3: slop-local 自定义插件（扩展点落地 + 首条规则 no-emoji）

**Files:**
- Create: `.agents/skills/slop-linter/engine/rules/index.ts`
- Create: `.agents/skills/slop-linter/engine/rules/rules/no-emoji.ts`
- Modify: `.agents/skills/slop-linter/engine/oxlintrc.json`（jsPlugins + rules 增项）
- Modify: `.agents/skills/slop-linter/engine/fixtures/sloppy.ts`（加 emoji 行）
- Modify: `.agents/skills/slop-linter/engine/selfcheck.sh`（加断言）

**Interfaces:**
- Consumes: Task 1/2 的 oxlintrc 与 selfcheck。
- Produces: 注册名 `slop-local` 的插件，规则全名 `slop-local/no-emoji`——这是 SR-006 的机械侧对应，也是"语义规则毕业进 JS 规则"的管道示范（SKILL.md/README 引用此模式）。

- [ ] **Step 1: fixtures 先加违规并确认 selfcheck 变红**

用 Edit 在 `fixtures/sloppy.ts` 末尾追加：

```ts
// rocket launch 🚀 — emoji demo for slop-local rule
export const emojiDemo = "done ✅";
```

跑 `bash engine/selfcheck.sh`，Expected: PASS（此刻 `slop-local/no-emoji` 尚未注册，emoji 行无人报——红的是"缺规则"这一事实，本步只确认基线）。

- [ ] **Step 2: 写插件入口与规则**

用 Write 工具创建 `engine/rules/index.ts`：

```ts
import noEmoji from "./rules/no-emoji";

export default {
  rules: {
    "no-emoji": noEmoji,
  },
};
```

用 Write 工具创建 `engine/rules/rules/no-emoji.ts`：

```ts
const EMOJI_RE = /\p{Extended_Pictographic}/u;

export default {
  meta: { type: "suggestion", docs: { description: "Reject emoji in code, comments and UI copy (SR-006)." } },
  create(context: any) {
    const report = (node: any, where: string) => {
      context.report({ node, message: `slop-local/no-emoji: emoji in ${where} is not allowed — use plain text` });
    };
    return {
      Literal(node: any) {
        if (typeof node.value === "string" && EMOJI_RE.test(node.raw ?? "")) report(node, "string literal");
      },
      "Program:exit"(node: any) {
        for (const c of context.sourceCode.getAllComments()) {
          if (EMOJI_RE.test(c.value)) report(node, "comment");
        }
      },
    };
  },
};
```

- [ ] **Step 3: 注册进 oxlintrc.json**

用 Edit 修改 `engine/oxlintrc.json`：jsPlugins 数组加 `{ "name": "slop-local", "specifier": "./rules/index.ts" }`；rules 对象加 `"slop-local/no-emoji": "error"`。

- [ ] **Step 4: selfcheck 加断言并确认全绿**

用 Edit 在 selfcheck.sh part1 的规则循环里加 `slop-local/no-emoji`：

```bash
for rule in anti-slop/no-array-filter-map anti-slop/no-chained-type-assertions \
            anti-slop/no-runtime-typeof anti-slop/require-safety-comment-for-type-assertion \
            slop-local/no-emoji; do
```

```bash
bash /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/selfcheck.sh
```

Expected: `selfcheck PASS`，含 `slop-local/no-emoji fires`。若插件加载失败（TS 入口/jiti 问题）→ 对照 spec §13 验证① 的结论与降级路径处理，显式失败不许静默跳过。

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/slop-linter/engine
git commit -m "feat(slop-linter): add slop-local plugin with no-emoji rule (SR-006 mechanical counterpart)"
```

---

### Task 4: semantic-rules.md 种子

**Files:**
- Create: `.agents/skills/slop-linter/semantic-rules.md`

**Interfaces:**
- Produces: SKILL.md（Task 5）Order 第 3 步的必读文件；README（Task 6）定义其格式契约。文件本身是"个人判定依据"，属更新合同 B，永不整替（spec §12.1）。

- [ ] **Step 1: 取当前 rev 作 upstream-rev**

```bash
git -C /Users/yangjun/Desktop/my-ai rev-parse --short HEAD
```

记为 `<REV>`（种子写入时的本仓状态；同事拷走后按 README 指引替换为他们的 clone rev）。

- [ ] **Step 2: 写种子文件**

用 Write 工具创建 `.agents/skills/slop-linter/semantic-rules.md`：

```markdown
---
upstream-rev: <REV>
---
# slop-linter 语义规则库（唯一权威源）

格式：`SR-ID | severity | 规则 — 判定要点`。severity：`error`（计入 verdict）/ `advisory`（仅报告）。
种子段（SR-0xx）随上游维护；个人追加从 SR-101 起；显式拒绝的规则移入 rejected 段（tombstone，同步不回塞）。
变更纪律：一律提议-确认后写入，单独成 commit（spec §7.1）。

## 种子段（SR-0xx）

SR-001 | error | 注释只写非显然 WHY — WHAT 复述、任务引用（"for issue#123"）、多段 docstring 均违规；删掉不令读者困惑的注释就该删
SR-002 | error | 无防御性兜底 — 不可能场景的 try/catch、null/undefined 检查、fallback 分支；信任内部契约，边界校验只留系统边界（用户输入、外部 API）
SR-003 | error | 禁过早抽象 — 单实现接口、预防性泛化/DI；三行相似优于提前抽象
SR-004 | error | 禁无需求兼容层 — backward shim、feature flag、re-export 转发、"// removed" 尸体注释
SR-005 | error | 命名业务语义化 — data1/tmp/handler2/res2 类命名违规
SR-006 | error | 禁 emoji 与 AI 腔 — 代码、注释、UI 文案均适用（机械侧对应 slop-local/no-emoji，重复命中以机械层为准）
SR-007 | error | 禁空实现与假文档 — 空函数、描述与实现不符的注释、膨胀注释

## 个人追加段（SR-1xx+）

（空 — 运行时纠正经提议-确认后追加于此）

## rejected

（空 — 格式：`SR-0xx: rejected — 理由`）
```

- [ ] **Step 3: 请用户过目种子（内容闸门）**

向用户展示 7 条种子，确认/改/删（vendor 哲学：拷进来就是你的）。用户改动直接 Edit 进文件后再 commit。

- [ ] **Step 4: Commit**

```bash
git add .agents/skills/slop-linter/semantic-rules.md
git commit -m "feat(slop-linter): seed semantic-rules.md with SR-001..007"
```

---

### Task 5: SKILL.md（编排层）

**Files:**
- Create: `.agents/skills/slop-linter/SKILL.md`

**Interfaces:**
- Consumes: `engine/runner.sh` 契约（Task 2）、`semantic-rules.md`（Task 4）、harness-data 路径约定（`<hd>/tasks/<task>/`、`<hd>/<alias>/notes.md`、`<hd>/<alias>/config.sh` 的 `HARNESS_LINT_CMD`——均为 harness-dev 既有约定，文本依赖非代码依赖）。
- Produces: Qoder 自动发现的可调用技能 `slop-linter`（真身直放 `.agents/skills/` 即注册，已核实）。

- [ ] **Step 1: 写 SKILL.md**

用 Write 工具创建 `.agents/skills/slop-linter/SKILL.md`：

```markdown
---
name: slop-linter
description: AI-slop detection for completed requirement development. Use when the user asks to lint or slop-check a finished requirement, branch or PR ("lint 这个需求", "跑一下 slop 检测", "check this branch for slop"), or names a repo for standalone detection. Two layers - deterministic oxlint+anti-slop scan via engine/runner.sh, then agent semantic review against semantic-rules.md - producing a tiered report and verdict, with an optional in-session fix loop after explicit user confirmation.
version: 1.0.0
---

# Slop Linter — post-development slop detection

You are the **detector**. Role isolation: you never judge code you wrote in this
session; you judge from rules + diff + findings only (same discipline as
harness-testing).

## Step 0: locate

Resolve this skill's real directory (symlink-safe):

```bash
AGENT="$(cd "$(dirname "$(readlink -f <this-SKILL.md-path>)")" && pwd)"
```

- Engine: `$AGENT/engine/`（runner.sh · oxlintrc.json · rules · fixtures）
- Semantic rules: `$AGENT/semantic-rules.md`
- Workspace mode only（目标仓库无 .harness install-mode 支持，遇到时说明并仍按直连模式跑）

## Invocation modes

- **Task mode** — 用户点名 harness 任务：repo 从 `<hd>/tasks/<task>/current.md` 解析
  （`<hd>` = harness-data 根，kit 的同级目录；解析不出就问用户，勿猜）。
  findings 与报告写 `<hd>/tasks/<task>/lint-findings.json` 与 `lint-report.md`。
- **Direct mode** — 用户给仓库路径或说"当前仓库"：base 默认 origin 默认分支 merge-base；
  报告呈现于对话，用户指定路径才落文件。

## Order（严格顺序）

1. 解析 repo + base（或用户给的文件集）。先跑第 2 步再看别的。
2. 机械层：
   `bash $AGENT/engine/runner.sh --repo <repo> [--base <base>] --out <findings.json>`
   - oxlint 缺失 → 告知一次性 `cd $AGENT/engine && npm install`，停。
   - 插件加载失败 / 非法 JSON → **显式失败报告**（spec §11：静默降级 = 假阴性）。
   - `nothingToLint: true` → 报告 "nothing to lint"，正常终止。
3. 读规则：`semantic-rules.md` 全文（每次运行必读，不跨会话缓存）+
   `<hd>/<alias>/notes.md` 存在 "lint" 段则并入（仓特有规则）。
4. 读 diff 全文：`git -C <repo> diff <base>...HEAD`。
5. 新旧行区分：诊断行号落在该文件 changedLines 内 → 计入 verdict；落在存量行 →
   advisory（列出、注明"非本次引入"、不阻卡）。
6. 语义审查：逐条 SR-* 与仓特有规则对照**新增/修改行**。每条 finding 必须含
   规则 ID + file:line + 原文引用 + 建议修法；低置信 → warn 档。
7. 写报告（三档表：error / warn / advisory + verdict + 修复循环记录区）。
8. verdict：**clean** = 零 error 档；**needs-fix** = ≥1。needs-fix → 列修复清单，
   问用户"会话内修 / 仅报告"。
9. 修复循环（用户确认后）：
   - 先 autofix：`cd <repo> && $AGENT/engine/node_modules/.bin/oxlint --config
     $AGENT/engine/oxlintrc.json --disable-nested-config --fix <files>`
   - 剩余项逐个手修（小步、最小 diff）。
   - 出口条件（两查都过才算完）：复跑 runner error 档清零 **且** 目标仓自身 lint 通过
     （`HARNESS_LINT_CMD` 取自 `<hd>/<alias>/config.sh`，空则跳过并注明）。
   - 有界：修复轮 ≤3；同一 finding 3 轮不消 → needs_human，出 ESCALATED handoff
     （路径/证据/当前假设/建议下一步）。
   - **不自动 commit**：修完汇总改动，建议 slop 清理单独成 commit，由用户决定。
10. lessons：漏判/误判 → 按 spec §7.1 提议（SR 增改或毕业进 slop-local JS 规则），
    用户确认后写入并单独 commit。
```

- [ ] **Step 2: 人工核对（无机械测试，走评审清单）**

对照 spec §8 逐条核对：两种模式齐全、Order 10 步齐全、verdict 定义与 §9 一致、修复循环边界与 §10 一致（≤3 轮、出口两查、不自动 commit）、错误处理与 §11 一致（显式失败三处）、lessons 与 §7.1 一致。发现缺项 → Edit 补齐。

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/slop-linter/SKILL.md
git commit -m "feat(slop-linter): add SKILL.md orchestration layer (task/direct modes, verdict, fix loop)"
```

---

### Task 6: README（边界契约 + 更新流程 + 推广）

**Files:**
- Create: `.agents/skills/slop-linter/README.md`

**Interfaces:**
- Consumes: Task 1-5 产出的全部契约。
- Produces: 推广/多人同步的文档基础（spec §12）；同事拷走后的接入说明。

- [ ] **Step 1: 写 README.md**

用 Write 工具创建 `.agents/skills/slop-linter/README.md`：

```markdown
# slop-linter

需求开发完成后的 AI-slop 检测 agent：确定性机械层（oxlint + anti-slop + slop-local）
+ agent 语义层（semantic-rules.md）。设计 spec 见
`docs/superpowers/specs/2026-10-10-slop-linter-design.md`。

## 边界契约

- **engine/runner.sh**：`--repo <path> [--base <ref>] [--files <p1,p2>] [--out <file>]`
  → findings JSON（files+changedLines+diagnostics+oxlintExitCode）。
  exit 0 clean/empty · 1 error 档 · 2 用法/环境失败。对目标仓库只读。
- **规则宿主**：机械层全部在 engine（oxlintrc.json 唯一调优点）；语义层唯一源是
  semantic-rules.md（格式：`SR-ID | severity | 规则 — 判定要点`，含种子段/个人段/
  rejected 段，frontmatter 记 upstream-rev）。
- **零仓库侵入**：目标仓库不装依赖、不改配置、不提交文件；唯一写操作是修复循环
  且须用户显式确认。
- **自检**：`bash engine/selfcheck.sh` —— 规则调整、插件升级、engine 整替后必跑。

## 更新（两份合同，spec §12.1）

- **可整替（全域无个人状态）**：runner.sh、fixtures/、vendored anti-slop/、
  package.json 的版本 pin。整替后跑 selfcheck。
- **永不整替（个人判定依据）**：engine/rules/、oxlintrc.json 调级、
  semantic-rules.md。只接受条目级整合 + 提议-确认。

### vendored anti-slop 更新流程（六律，agent 会话执行）

1. 新源 clone 到临时目录，**单独 staging**，不直接覆盖。
2. 三方合并，基准 = `anti-slop/VENDORED.md` 记录的 revision。
3. 本地定制保留（我们的纪律是不改 vendored，此项通常为空）。
4. 冲突 → 问询用户，不自动裁决。
5. 更新后回写 VENDORED.md 的 revision 与日期。
6. 绝不 force-replace；更新后 selfcheck 必须绿。

## 推广 / 接入

- **拷贝整个 `.agents/skills/slop-linter/` 目录**即 standalone：`cd engine && npm install`
  一次即活（package.json 已精确 pin）。
- **接入自己的 harness/流程**：只对接 runner.sh 窄接口；本仓 SKILL.md 是编排参考实现。
- **同事首次接入**：拷目录后把 semantic-rules.md 的 `upstream-rev` 改成你拷贝时的
  本仓 rev；种子规则照你的审美改（vendor 哲学：拷进来就是你的）。
- **多人规则同步**（将来落地）：拉上游 → 对比 upstream-rev 之后的规则 diff → 逐条
  adopt/reject（reject 写 rejected 段）→ 本地改过的种子冲突人工裁决。个人段（SR-1xx+）
  上游命名空间永不写入——结构性保证整文件覆盖不可能发生。
```

- [ ] **Step 2: 核对并 Commit**

核对 README 与 spec §12/§5.1/§15 无矛盾（接口、两份合同、六律、推广四条）。然后：

```bash
git add .agents/skills/slop-linter/README.md
git commit -m "docs(slop-linter): add README boundary contract, update procedure and promotion guide"
```

---

### Task 7: harness-dev wrap-up 提醒（harness-kit 唯一改动）

**Files:**
- Modify: `harness-kit/skills/harness-dev/SKILL.md`（§8 第 4 条后追加一句）

**Interfaces:**
- Produces: harness 流程与 slop-linter 的唯一交叉点（spec §14：一行文档提醒，不改引擎）。

- [ ] **Step 1: Edit 追加提醒**

用 Edit 工具，old_string：

```
4. Remind the user: acceptance must happen in a **separate session** using the
   harness-testing skill (role isolation; never self-accept in this session).
```

new_string：

```
4. Remind the user: acceptance must happen in a **separate session** using the
   harness-testing skill (role isolation; never self-accept in this session);
   optionally also run the slop-linter skill in a separate session for
   post-development AI-slop detection.
```

- [ ] **Step 2: Commit**

```bash
git add harness-kit/skills/harness-dev/SKILL.md
git commit -m "docs(harness-kit): mention slop-linter in harness-dev wrap-up reminders"
```

---

### Task 8: 真实仓库冒烟（直连模式，只读）+ 收尾

**Files:**
- 无代码产出；产物是冒烟记录与（如有）spec 微调。

**Interfaces:**
- Consumes: Task 1-7 全部交付物。
- Produces: §15 验收的"直连模式至少跑一次"证据。

- [ ] **Step 1: 问用户指定冒烟目标**

问：哪个仓库当前正好 checkout 在 feature 分支上、可以**只读**冒烟（例如
conversations-frontend 若正在 CTOOL-719 分支）。不得为了冒烟切换别人工作区里的分支。

- [ ] **Step 2: 直连模式跑 runner**

```bash
bash /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/runner.sh --repo <用户给的仓库路径> --out /tmp/slop-smoke.json
jq '{dirty, nothingToLint, files: (.files | length), errors: ([.diagnostics[] | select(.severity == "error")] | length), total: (.diagnostics | length)}' /tmp/slop-smoke.json
```

Expected: 合法 JSON；`dirty` 字段如实反映工作树状态；若 nothingToLint 则换目标分支或改用 `--files` 指几个文件。向用户呈现 findings 摘要（error/warn/advisory 口径）。**全程不改目标仓库任何文件。**

- [ ] **Step 3: 全套终检**

```bash
bash /Users/yangjun/Desktop/my-ai/.agents/skills/slop-linter/engine/selfcheck.sh
ls .agents/skills/slop-linter/
git log --oneline -7
```

Expected: selfcheck PASS；目录含 SKILL.md、README.md、semantic-rules.md、engine/；7 个功能 commit 全部在本地（不 push）。

- [ ] **Step 4: 真实任务验收挂账（不在本计划内执行）**

spec §15 的"第一个真实需求全流程验收"（任务模式 + 修复循环 + lessons 回写）需要等下一个真实需求完成后触发——在总结里向用户明确这一点，建议下次 wrap-up 后开独立会话跑 slop-linter。

---

## Self-Review 记录

- **Spec coverage**：§3 架构→Task 1/2/3/5；§4 布局→File Structure 全量；§5.1-5.3→Task 1/2；§6 规则体系（含 .vue 兜底）→Task 1 spike③/Task 2 .vue 断言分支；§7 规则库与格式→Task 4；§7.1 升级→SKILL.md Order 10 + README；§8 技能流程→Task 5；§9 verdict/报告→Task 5 Order 7-8；§10 修复循环→Task 5 Order 9；§11 错误处理→Task 5 Step 0/Order 2 + runner die；§12 更新与分发→Task 6 README；§13 spike→Task 1；§14 边界（harness-dev 一行）→Task 7；§15 测试验收→Task 2 selfcheck + Task 8；§16 顺序→任务顺序一致。无缺口。
- **Placeholder scan**：`<V>`（版本号）与 `<REV>`（upstream rev）均为 Step 内用命令解析后回填的运行时值，非计划占位；Task 8 Step 2 已清除占位命令，仅剩 `<用户给的仓库路径>` 为 Step 1 向用户征集的输入，两处均已写明来源。
- **Type consistency**：runner 参数四枚（--repo/--base/--files/--out）在 Task 2/5/6/8 一致；插件名 slop-local 全文一致；findings JSON 键（repo/base/head/dirty/nothingToLint/files/changedLines/diagnostics/oxlintExitCode）Task 2 定义、Task 5/8 消费一致；severity=="error" 判定在 Task 2 runner 与 Task 8 jq 一致。
