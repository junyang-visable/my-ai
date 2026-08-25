---
name: harness-dev
description: 个人 harness 工具集的跨仓库开发总控入口。当用户在工具集仓库（my-ai）会话里要开发其他代码仓库（如"用 harness 开发 X 仓库 / 给 X 仓库做 Y / 跨仓库开发"），或提到 harness-dev、注册新 workspace 时使用。负责定位 kit、注册或切换目标仓库、体检、建任务、以实现者角色进入编码循环，收尾沉淀经验到本仓库并提示独立验收。
version: 1.0.0
---

# Harness Dev — 跨仓库开发总控

你从**个人工具集仓库**驱动任意目标仓库的开发：引擎、任务状态、经验全部沉淀在 kit，
目标仓库可以零安装（workspace 模式）。本技能只做**实现者**职责，不做验收。

## 1. 定位 kit

kit 根 = 本 skill 物理目录向上 4 级（`adapters/qoder/skills/harness-dev`）。
软链部署时先解析真实路径再上溯：

```bash
cd "$(dirname "$(readlink -f <本SKILL.md路径>)")/../../../.." && pwd
```

兜底（换机后改这一行）：`/Users/yangjun/Desktop/my-ai/harness-kit`。
下文用 `<kit>` 指代它。

## 2. 确定目标仓库

- 用户给了**别名**：`bash <kit>/harness use <alias>`（不存在则展示 `harness list` 并问是否注册）
- 用户给了**路径**：`bash <kit>/harness add <alias> <path>`（alias 取仓库名，重名加后缀）
- **没给**：`bash <kit>/harness list` 展示全部让用户选；一个都没有就引导注册
- 若目标仓库根存在 `.harness/config.sh`（install 模式），告知用户两种模式皆可，按其意愿选择

## 3. 新 workspace 引导（仅首次注册时）

1. 读目标仓库的 `package.json` / `Makefile` / `pyproject.toml` 等，**推断**
   lint / typecheck / build / test 命令，写进 `workspaces/<alias>.conf.sh`，
   并把推断依据告诉用户请其确认（不确定的留空，留空阶段自动跳过）。
2. `bash <kit>/harness doctor` 体检；`bash <kit>/harness validate selfcheck` 确保护栏不是纸糊的。
3. 仓库的栈与坑随手记进 `workspaces/<alias>/notes.md`；E2E 需求出现时再补
   `workspaces/<alias>/context/e2e-context.md`。

## 4. 任务与写权限

- **写权限前置检查**：目标仓库不在当前 Qoder 工作区时，写文件会被沙箱拦。
  开工前提醒用户把目标仓库加入工作区（Add Folder to Workspace），不要反复试错。
- `bash <kit>/harness task new <需求名>` 建任务；已有同名任务则先读其
  `current.md`（当前阶段 + 唯一下一步）续跑，不要另起炉灶。
- 新任务且跨文件/跨模块：先填任务 `spec.md`（需求边界 / 方案 / 影响文件 / 计划），
  用户确认后再进编码循环；单文件小改可跳过，口头澄清即可。

## 5. 编码循环（实现者角色）

与 harness-coding 技能同一套纪律，核心如下：

- 先澄清需求与验收边界再动手；不清楚就停下来问。
- 判断走不走全套（11020656025）：跨 3 文件以上 / 异步并发状态机 / 外部系统集成 → 全套；
  单文件 bugfix / 加日志 / 改文案 → 直接改。
- 单测 TDD（可单测的逻辑改动适用，与走不走全套无关）：先写测试跑一次确认 RED
  （失败断言记入任务 `history.md`），再实现变绿；bugfix 先写能复现 bug 的失败测试。
  纯文案/样式不强制。
- 小步改；完成前跑唯一验证入口：

  ```bash
  bash <kit>/harness validate        # 跨文件改动加 --strict
  ```

- 阻断级不过 = 没完成。**禁止**删断言 / 改测试预期 / 加 `@ts-ignore` / 新建测试文件凑绿；
  认为测试本身有误就停下说明理由。build 不可跳过。
- 失败就收证据变成下一轮输入：`bash <kit>/harness evidence <需求名> <layout|api|render|generic>`

## 6. 收尾

1. 更新任务 `current.md`（当前阶段 + 唯一下一步）与 `history.md`（只追加一行）。
2. 按 `<kit>/.harness/rubric/evidence-template.md` 申报完成证据（数字可复核，未覆盖范围诚实申报）。
3. **经验回写**（这就是工具集的价值所在，别省略）：
   - 该仓库的坑 / 命令实测 / 约定 → `workspaces/<alias>/notes.md`
   - 换个仓库仍成立的做法 → `<kit>/playbooks/<主题>.md`（从 `_template.md` 起稿）
   - 任务过程细节 → 任务 `history.md`
4. 提醒用户：验收须**另开会话**用 harness-testing 技能（角色信息隔离，勿在本会话自验）。

## 三态退出

- `success`：validate 全绿 + 证据齐 → 交独立会话验收。
- `failed`：同一错误连续 3 轮无进展 → 停止盲试。
- `needs_human`：产出 ESCALATED 交接包（已试路径、失败证据、当前最可信假设、建议下一步）。
