# AGENTS.md — <项目名> 的 Agent 契约层

> 这是给 AI agent 看的第一份、也是常驻上下文里唯一的项目手册。
> 原则（11020601776 / 11020603220）：**只做索引与红线，控制在 ~100 行 / ~2.5K tokens**。
> 细节一律下沉到 `docs/` 和 `.harness/`，按需加载，不写进这里。
> 超过 32K tokens 上下文后模型正确率显著下降（11020456085），所以这份越短越好。

## 30 秒速览

- 这是什么项目：<一句话>
- 技术栈：<语言 / 框架 / 包管理器>
- 怎么跑起来：`<install>` → `<dev>`

## 唯一的验证入口（必须记住）

任何改动完成前，跑这一条，绿了才算完成：

```bash
bash .harness/feedback/validate.sh
```

- 它合成了 lint → typecheck → arch → build → test，并按三级门禁给结论。
- 阻断级不过 = 没完成。**不要**通过删断言 / 改测试预期 / 加 `@ts-ignore` 来凑绿。
- 声称"完成"时，按 `.harness/rubric/evidence-template.md` 附证据。

## 红线（阻断级，违反必被 validate 拦）

1. 领域层不得依赖基础设施层，跨层依赖走接口反转（规则见 `.harness/feedback/lint-arch.sh`）。
2. `build` 不可跳过；`lint` 零 warning / error；测试全绿（11020656025）。
3. 冒烟测试受断言锁保护，改动需 `// @lock-bypass` + 提交说明，留审计痕迹。
4. <按项目补充：禁止直连生产库 / 禁止提交密钥 / 必须走某网关 …>

## 走不走全套的判据（11020656025）

- **走全套 validate**：跨 3 个以上文件、涉及异步并发状态机、涉及外部系统集成。
- **直接对话改**：单文件 bugfix、加日志、改文案。
- 纯类型 / 文档 / 测试改动可跳过视觉验证，但仍需过 validate。

## 按需加载的知识（不要一次性全读）

- 架构与模块边界 → `docs/ARCHITECTURE.md`
- 本地开发 / 调试 / 环境变量 → `docs/DEVELOPMENT.md`
- E2E 用例上下文（页面入口 / 测试账号 / 稳定选择器）→ `.harness/context/testing/e2e-context.md`
- 验收标准四级 Rubric → `.harness/rubric/rubric-template.md`
- 防谎报三件套 → `.harness/rubric/anti-false-reporting.md`

## 循环层（多步任务时用）

一个需求的状态写在 `.harness/tasks/<需求名>/` 下：
`current.md`（当前阶段 + 唯一下一步）、`result.md`（有效结论 + 残留风险）、
`history.md`（只追加）、`evidence/`（截图 / 报告）。
换会话续跑时先读 `current.md`。

## MCP / 工具最小集

只接当前需求用得到的 MCP server。单个 server 20–30 个工具约占 4–6K tokens，
接 5 个≈25K tokens（200K 的 12.5%）且每轮常驻（11020603220）。不用的关掉。
