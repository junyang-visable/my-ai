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
# oxlint -f json 顶层是包装对象 {diagnostics:[...]}；code 为括号形式 anti-slop(<rule>)（spec §13 实测）
OUT="$("$OXLINT" --config "$CFG" --disable-nested-config -f json "$ENGINE_DIR/fixtures/sloppy.ts")"
for rule in 'anti-slop(no-array-filter-map)' 'anti-slop(no-chained-type-assertions)' \
            'anti-slop(no-runtime-typeof)' 'anti-slop(require-safety-comment-for-type-assertion)' \
            'slop-local(no-emoji)'; do
  if printf '%s' "$OUT" | jq -e --arg r "$rule" 'any(.diagnostics[]; .code == $r)' >/dev/null; then
    ok "$rule fires"
  else
    miss "$rule does NOT fire (tune fixture until deterministic)"
  fi
done
CLEAN="$("$OXLINT" --config "$CFG" --disable-nested-config -f json "$ENGINE_DIR/fixtures/clean.ts")"
if printf '%s' "$CLEAN" | jq -e '.diagnostics | length == 0' >/dev/null; then ok "clean.ts zero findings"; else miss "clean.ts has findings"; fi

VUE_OUT="$("$OXLINT" --config "$CFG" --disable-nested-config -f json "$ENGINE_DIR/fixtures/sloppy.vue")"
if printf '%s' "$VUE_OUT" | jq -e --arg r "anti-slop(no-runtime-typeof)" 'any(.diagnostics[]; .code == $r)' >/dev/null; then
  ok "jsPlugins covers .vue script blocks (spec §13 实测已证实)"
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
printf 'export const one = 1;\nexport const flag = typeof one === "object";\nexport const three = 3;\n' > "$TMP/a.ts"
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
