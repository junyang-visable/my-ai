# workspace: visable-plugin-marketplace —— 仓库专属配置（覆盖 .harness/config.sh 的默认值）
HARNESS_REPO="/Users/yangjun/Desktop/visable-plugin-marketplace"

# 阻断级命令，按这个仓库的栈填；留空的阶段自动跳过
HARNESS_LINT_CMD=""            # 例: "pnpm -s lint"
HARNESS_TYPECHECK_CMD=""       # 例: "pnpm -s tsc --noEmit"
HARNESS_BUILD_CMD=""           # 例: "pnpm -s build"（前端硬门禁，不可跳过）
HARNESS_TEST_CMD=""            # 例: "pnpm -s test -- --run"

# 警告级
HARNESS_STYLE_CMD=""

# E2E / 冒烟集（断言锁作用域，相对仓库根；空格分隔可多条）
HARNESS_E2E_CMD=""             # 例: "pnpm -s cypress run --spec 'cypress/e2e/smoke/**'"
HARNESS_SMOKE_GLOB="cypress/e2e/smoke/**/*.cy.*"
