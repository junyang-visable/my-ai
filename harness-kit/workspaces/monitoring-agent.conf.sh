# workspace: monitoring-agent —— 仓库专属配置（覆盖 .harness/config.sh 的默认值）
HARNESS_REPO="/Users/yangjun/Desktop/projects-inc/monitoring-agent"

# 阻断级命令，按这个仓库的栈填；留空的阶段自动跳过
HARNESS_LINT_CMD=""            # 纯 Python 仓库，无 lint 配置（requirements.txt 仅 pytest）
HARNESS_TYPECHECK_CMD=""       # 无 mypy/pyright 配置
HARNESS_BUILD_CMD=""           # 无构建产物，纯脚本/技能仓库
HARNESS_TEST_CMD=".venv/bin/python -m pytest tests/ -v"  # 仓库自带 .venv（pytest 9.1.1）；CLAUDE.md "Running Tests" 段

# 警告级
HARNESS_STYLE_CMD=""

# E2E / 冒烟集（断言锁作用域，相对仓库根；空格分隔可多条）
HARNESS_E2E_CMD=""             # 例: "pnpm -s cypress run --spec 'cypress/e2e/smoke/**'"
HARNESS_SMOKE_GLOB="cypress/e2e/smoke/**/*.cy.*"
