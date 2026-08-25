#!/usr/bin/env python3
# =============================================================================
# .harness/feedback/lock-tests.py — 断言锁
# -----------------------------------------------------------------------------
# 记录冒烟测试「函数体的 SHA 基线」，之后若函数体被改动而未走正规放行流程，
# verify 返回 exit 2。目的是堵住「改测试预期 / 删断言来凑绿」这条路。
# 依据 11020729209（lock-smoke-tests.py：SHA 基线，不符 exit 2，放行留审计痕迹）。
#
# 用法:
#   lock-tests.py update           扫描冒烟集，(重)写基线
#   lock-tests.py verify           校验；有未授权改动 => exit 2
#   lock-tests.py list             打印当前基线内容
#
# 放行改动（二选一，都留痕）:
#   1) 环境变量:  HARNESS_LOCK_BYPASS=1 lock-tests.py verify
#   2) 在测试块内加注释 `@lock-bypass <原因>`，再 update 刷新基线
#
# 冒烟集范围由 config.sh 的 HARNESS_SMOKE_GLOB 决定（空格分隔多个 glob）。
# 不限栈：识别 JS/TS 的 it()/test() 块与 Python 的 def test_ 块，其余类型退化为整文件哈希。
# =============================================================================
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS_DIR = os.path.dirname(HERE)
# workspace 模式下由 harness CLI 注入每仓库独立的基线路径，避免多仓库互相覆盖；
# install 模式默认落在引擎目录内。
BASELINE = os.environ.get("HARNESS_LOCK_BASELINE") or os.path.join(
    HERE, ".lock-baseline.json"
)

SMOKE_GLOB = os.environ.get(
    "HARNESS_SMOKE_GLOB", "cypress/e2e/smoke/**/*.cy.*"
).split()
BYPASS_ENV = os.environ.get("HARNESS_LOCK_BYPASS", "") not in ("", "0", "false")


def iter_files():
    seen = set()
    for pat in SMOKE_GLOB:
        for f in glob.glob(pat, recursive=True):
            if os.path.isfile(f) and f not in seen:
                seen.add(f)
                yield f


def norm(s):
    # 归一化空白，避免纯格式化触发锁
    return re.sub(r"\s+", " ", s).strip()


def sha(s):
    return hashlib.sha256(norm(s).encode("utf-8")).hexdigest()[:16]


def extract_blocks(path):
    """返回 [(block_name, body_text, has_bypass), ...]"""
    text = open(path, encoding="utf-8", errors="replace").read()
    blocks = []
    ext = os.path.splitext(path)[1]

    if ext in (".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs"):
        # 匹配 it('name' / test("name" 起始，做花括号配平
        for m in re.finditer(r"""\b(it|test)\s*\(\s*['"`]([^'"`]+)['"`]""", text):
            name = m.group(2)
            i = text.find("{", m.end())
            if i == -1:
                continue
            depth, j = 0, i
            while j < len(text):
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            body = text[i : j + 1]
            blocks.append((name, body, "@lock-bypass" in body))
    elif ext == ".py":
        lines = text.splitlines(keepends=True)
        i = 0
        while i < len(lines):
            m = re.match(r"(\s*)def (test_\w+)\s*\(", lines[i])
            if m:
                indent = len(m.group(1))
                name = m.group(2)
                body = [lines[i]]
                k = i + 1
                while k < len(lines):
                    ln = lines[k]
                    if ln.strip() and (len(ln) - len(ln.lstrip())) <= indent:
                        break
                    body.append(ln)
                    k += 1
                btext = "".join(body)
                blocks.append((name, btext, "@lock-bypass" in btext))
                i = k
                continue
            i += 1

    if not blocks:
        blocks.append(("<whole-file>", text, "@lock-bypass" in text))
    return blocks


def snapshot():
    snap = {}
    for f in sorted(iter_files()):
        snap[f] = {name: sha(body) for name, body, _ in extract_blocks(f)}
    return snap


def cmd_update():
    snap = snapshot()
    json.dump(snap, open(BASELINE, "w"), indent=2, ensure_ascii=False)
    n = sum(len(v) for v in snap.values())
    print(f"lock: baseline 已写入 {BASELINE}（{len(snap)} 文件 / {n} 测试块）")
    return 0


def cmd_verify():
    if not os.path.exists(BASELINE):
        print("lock: 无基线，视为通过（先跑 `lock-tests.py update`）")
        return 0
    base = json.load(open(BASELINE))
    cur = {}
    bypass_names = set()
    for f in sorted(iter_files()):
        cur[f] = {}
        for name, body, has_bypass in extract_blocks(f):
            cur[f][name] = sha(body)
            if has_bypass:
                bypass_names.add(f"{f}::{name}")

    violations = []
    for f, blocks in base.items():
        for name, h in blocks.items():
            key = f"{f}::{name}"
            now = cur.get(f, {}).get(name)
            if now is None:
                violations.append(f"删除/改名: {key}")
            elif now != h and key not in bypass_names:
                violations.append(f"函数体被改: {key}")
    # 新增块不算违规（允许固化新用例）

    if not violations:
        print("lock: verify 通过，冒烟集未被非法改动")
        return 0
    print("lock: 检测到未授权的冒烟测试改动:")
    for v in violations:
        print("  - " + v)
    if BYPASS_ENV:
        print("lock: HARNESS_LOCK_BYPASS=1 已放行（审计：本次绕过断言锁）")
        return 0
    print("lock: 若确需改动，加 `@lock-bypass 原因` 注释后重新 update，"
          "或用 HARNESS_LOCK_BYPASS=1 放行。")
    return 2


def cmd_list():
    if not os.path.exists(BASELINE):
        print("(无基线)")
        return 0
    print(open(BASELINE).read())
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    return {"update": cmd_update, "verify": cmd_verify, "list": cmd_list}.get(
        cmd, cmd_verify
    )()


if __name__ == "__main__":
    sys.exit(main())
