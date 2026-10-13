---
name: release-approval
description: 为待发布需求生成审批邮件(.eml)并在 Confluence System Change Log database 创建发布记录行。Use when 用户要发审批邮件、发布审批、release approval、"帮我发 XX 需求的发布审批"、要在 System Change Log 加发布记录，或提到需求发布前的审批邮件流程。
---

# Release Approval

## Overview

发布一个需求前做两件事：

1. 按团队模板生成审批邮件 `.eml` 草稿（收件人/主题预填，`X-Unsent: 1` 草稿标记）。**skill 只创建草稿，绝不发送**——生成后 `open` 打开落到邮件客户端，检查与点发送完全由用户完成。
2. 在 Confluence database「System Change Log」(id `376700933`，PRODTECH 空间) 创建一行发布记录。

Step 0：以 harness 加载本技能时给出的 base directory 为 `$SKILL_DIR`（若该路径是 symlink，用 `readlink -f` 解析真实路径再拼接 scripts/config 路径）；本仓库注册路径为 `/Users/yangjun/Desktop/my-ai/.agents/skills/release-approval`。

## 配置（模板入库、实配置本地、缺失静默回退）

- `config.template.json`：入库的模板，含占位默认值。
- `config.json`：本地实配置（已被 `.gitignore` 忽略），**存在则优先生效**；不存在或某键缺失时回退模板对应值，不要报错。
- 读取方式：`node -e "const c=require('$SKILL_DIR/config.json')" 2>/dev/null || node -e "const c=require('$SKILL_DIR/config.template.json')"`，逐键合并。

关键配置键：

- `email.to` / `email.cc` / `email.from`：固定收件人。**to 为空时先问用户本次收件人**，用户给出后顺手写入 `config.json`（下次免问）。条目支持 `"Name <addr>"` 或纯地址两种写法，脚本自动处理显示名引号/RFC2047 编码。
- `defaults`：group / executor / qaEngineer / canRollback / trackingImpacted 的默认值。
- `database.url`：database 页面地址。`database.columns`：System Change Log 列名 → 字段映射（首次使用时采集，见第 3 步）。

## 第 1 步：收集字段

调用参数给多少用多少；缺关键字段（name、prUrl、reviewer）才追问，其余用 config 默认值。

| 字段 | 来源 | 说明 |
|---|---|---|
| name | 必须有 | 发布名，如 "Remove quick editor ab experiment" |
| prUrl | 必须有 | Git PR 链接 |
| reason | 建议有 | 变更原因，一句话 |
| reviewer | 必须有 | Code reviewer 姓名 |
| group | config 默认 Supplier | |
| executor | config 默认 Jun Yang | |
| qaEngineer | config 默认 Jun Yang | |
| canRollback | config 默认 Yes | |
| trackingImpacted | config 默认 No | Yes 时必须拿到 trackingNote 与 regressionCheck，否则追问 |
| prReviewed | 默认 true | 若 PR 尚未被 review，先提醒用户补 review 再继续（审批邮件里此项应为 ✅） |

## 第 2 步：生成审批邮件

1. 把合并后的字段写成 `/tmp/release-approval-fields-<slug>.json`（含 `to`/`cc`）。
2. 运行：

   ```
   node $SKILL_DIR/scripts/build-eml.mjs <fields.json> -o "$HOME/Desktop/<slug>-release-approval.eml"
   ```

3. 脚本 stdout 输出 `OK eml written: <路径>` + Subject/To/Cc 摘要即成功；`ERROR:` 开头则按提示补字段重跑。
4. 生成成功后默认 `open <eml路径>`：邮件客户端立即打开该草稿（Outlook 识别 `X-Unsent: 1` 为可编辑草稿；Mac Mail 为消息预览），由用户核对后自行发送。

## 第 3 步：System Change Log 创建发布记录行

背景（勿重试已排除的路由）：官方公开 API 无 database 行级操作（CONFCLOUD-77328 open，`/items` 路由 404）；database 前端是 sandbox iframe 独立应用，browser-use 的 snapshot/click/脚本注入均无法触达 iframe 内部。**已验证可行的机制：Qoder 主应用（`com.qoder.app`）的 AX 树会暴露内置浏览器 webview 的 web 内容**——用 computer-use 对 `com.qoder.app` 做 AX 元素读写；AX 不可用时退化到截图坐标点击。

1. browser-use navigate 到 `database.url` 加载页面；报 `NATIVE_BROWSER_VIEWPORT_UNAVAILABLE` 时请用户打开内置浏览器面板（加载不受影响，但可见面板是 AX 暴露与截图验证的前提）。若跳到 id.atlassian.com 登录页，请用户在受控窗口重登。
2. computer-use `getAppState({app:"com.qoder.app"})`：确认 AX 树含「System Change Log」「Add entry」且面板可见；不可见则请用户把内置浏览器面板切回前台，重新采集。
3. 点击「Add entry」→ 表尾出现新空行（2026-10-12 实测）。`config.database.columns` 已采集（12 列：Date / Team / Group / Reasons for the change / Change executor / Change Type / Can it be rolled back if it fails? / Status / Actual start time of change / Change details: Git PR / Others / Code Reviewer / QA Engineer）；若列头有出入，以当次 AX 列头为准并更新 config。
4. 逐格填写，按列映射：
   - **元素索引跨 capture 漂移**——每次操作的索引只取自上一步返回的最新状态，绝不复用更早 capture 的索引（曾因漂移点错面板）。
   - person 列（executor/reviewer/QA）输入姓名后从候选中选；select 列从下拉选。已观测选项：Team=Front-end/Back-end；Group=Buyer Group/Connection Group/UG Group（Supplier 侧选项未观测到，首次录入确认）；Change Type=Tech Project/Biz Project/Online Fix；Status=Success (verified&monitored)/Fail - Rolled back。拿不准的选项问用户，不要猜。
   - Change details: Git PR / Others 单元格支持多条链接条目，填 PR 链接。
5. 验证：再次 `getAppState` 确认新行各格内容与预期一致。
6. 兜底：AX/坐标均失败时，把按列组织的记录内容完整输出到对话 + `open` database 页面让用户手动粘贴，汇报标注「行创建：手动」。
7. 平台约束（auto 模式实测）：行创建/删除动作会被分类器拦截并要求**动作时打字确认**——提前告知用户确认一次，这是平台行为不是 skill 闸门。测试行清理：行内菜单 Delete，删除前同样需用户确认。

## 第 4 步：汇报

- eml：绝对路径 + 主题 + 收件人（等用户自行发送）。
- 行：computer-use 成功（附验证截图已确认）或手动兜底。

## Resources

- `scripts/build-eml.mjs`：字段 JSON → RFC822 `.eml`（HTML 三列表格正文，✅/`\` 状态列，主题 RFC2047 编码）。prUrl 支持单条 URL 或数组（元素为 URL 字符串 / `{text,url}` / `{header}`，每条一行 `<br>`）用于多 PR 发布。缺 name/prUrl/reviewer/to 时 exit 1。
- `config.template.json` / `config.json`：见「配置」。
