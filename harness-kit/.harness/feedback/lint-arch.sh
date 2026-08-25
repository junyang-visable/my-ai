#!/usr/bin/env bash
# =============================================================================
# .harness/feedback/lint-arch.sh — 架构依赖违规检查（阻断级）
# -----------------------------------------------------------------------------
# 不限栈的实现：用 grep 规则匹配「不该出现的跨层依赖」。
# 每条规则一行，格式:  <被保护的路径 glob>\t<禁止匹配的正则>\t<人话原因>
# 命中 => 打印 file:line + 原因 + 修复建议，exit 1。
#
# 真实项目里可把这里换成 dependency-cruiser / import-linter / go list 等原生工具，
# validate.sh 只关心退出码与「file:line | reason | fix」格式，不关心实现。
#
# 对齐: 11020729209（阻断级只留架构依赖违规等硬红线；反馈=文件行号+原因+修复）
# =============================================================================
set -uo pipefail
shopt -s globstar nullglob 2>/dev/null || true

SCAN_ROOT="${HARNESS_ARCH_SCAN_ROOT:-.}"

# ---- 规则表：按需在这里增删。默认给一条通用「领域层不得依赖基础设施层」示例 ----------
# 用真实的 TAB 分隔三列。
RULES=$(cat <<'RULES'
src/domain/**	(from|import|require).*(infra|infrastructure)/	领域层禁止直接依赖基础设施层（应通过接口/端口反转）
src/**	FORBIDDEN_CROSS_LAYER	命中显式跨层禁用标记
RULES
)

fail=0
c_red=$'\033[31m'; c_dim=$'\033[2m'; c_rst=$'\033[0m'

while IFS=$'\t' read -r glob pattern reason; do
  [ -z "${glob:-}" ] && continue
  # 展开 glob 到文件列表
  while IFS= read -r file; do
    [ -f "$file" ] || continue
    matches="$(grep -nE "$pattern" "$file" 2>/dev/null || true)"
    [ -z "$matches" ] && continue
    while IFS= read -r m; do
      line="${m%%:*}"
      printf "%sBLOCKING%s | arch | %s:%s | %s\n" "$c_red" "$c_rst" "$file" "$line" "$reason"
      printf "         %s↳ fix: 移除该依赖或经由抽象接口访问；确需例外请在评审中说明并调整规则%s\n" "$c_dim" "$c_rst"
      fail=1
    done <<< "$matches"
  done < <(cd "$SCAN_ROOT" 2>/dev/null && compgen -G "$glob" 2>/dev/null | sed "s#^#$SCAN_ROOT/#" || true)
done <<< "$RULES"

if [ "$fail" -ne 0 ]; then
  exit 1
fi
echo "arch: no cross-layer violations"
exit 0
