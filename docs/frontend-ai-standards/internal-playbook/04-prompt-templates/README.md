# Prompt 模板库

本目录提供 6 套可复制的 Prompt 模板，用于在 Cursor 等 AI IDE 中稳定产出符合团队规范的前端代码与文档。模板按「上下文 → 任务 → 约束 → 输出」组织，便于与项目 Repowiki、Cursor Rules 对齐。

## 四段式结构说明

每套模板在复制到对话中时，建议严格保留以下四个区块（可在 fenced 代码块内直接粘贴后按需填空）：

| 区块 | 作用 |
|------|------|
| **上下文注入** | 技术栈、目录约定、相关文档链接或摘要、参考文件路径，减少模型「猜」项目习惯的成本。 |
| **任务描述** | 单一、可验收的目标：改什么文件、做到什么程度、验收口径（含「不要做」的边界）。 |
| **约束语** | 必须遵守的工程约束：架构分层、i18n、样式变量、测试风格等，对应团队 Playbook / Cursor Rules。 |
| **输出要求** | 期望的交付形态：完整文件、diff、示例调用、类型定义、验证步骤等，避免只给片段无法落地。 |

使用方式：打开对应场景的 `.md` 文件 → 复制 **Prompt 模板** 整块 → 将 `[替换：…]` 或占位说明换成当前任务的具体信息 → 粘贴到 AI 对话；复杂任务可先在 **上下文** 中附上 Repowiki 节选或文件路径。

## 模板索引

| 模板文件 | 使用场景 |
|----------|----------|
| [component-generation.md](./component-generation.md) | 新建 Vue SFC 组件（`<script setup>` + TS），约定 Props/数据边界与 i18n。 |
| [page-refactoring.md](./page-refactoring.md) | 在**不改变行为与界面**的前提下拆分大文件、抽取 composable、整理结构。 |
| [api-integration.md](./api-integration.md) | 通过统一请求层（如 `composables/useRequest`）对接后端接口与类型。 |
| [style-adjustment.md](./style-adjustment.md) | 仅调整样式与响应式，不动 DOM 结构，颜色走 CSS 变量。 |
| [unit-test-generation.md](./unit-test-generation.md) | 基于 Vitest + Vue Test Utils 编写单元测试，强调行为与 mock 边界。 |
| [debug-analysis.md](./debug-analysis.md) | 按现象、预期、复现与报错定位根因，输出可验证的修复与多方案对比。 |

## 与 Repowiki / Cursor Rules 的配合

- **Repowiki**：在模板的「上下文」中引用 `02-repowiki` 下对应条目（组件规范、技术规范、路由等），避免与文档不一致。
- **Cursor Rules**：项目根目录或 `.cursor/rules` 中的约定（如禁止在组件内直连 API）应在「约束」中显式重申，强化模型遵守概率。

若某次对话需要组合多个模板（例如先 `debug-analysis` 再 `unit-test-generation`），建议分轮进行：每轮只保留一个主任务与一套输出要求，减少指令冲突。
