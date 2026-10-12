---
name: release-approval
description: 为待发布需求生成审批邮件(.eml)并在 Confluence System Change Log database 创建发布记录行。Use when 用户要发审批邮件、发布审批、release approval、"帮我发 XX 需求的发布审批"、要在 System Change Log 加发布记录，或提到需求发布前的审批邮件流程。
---

# Release Approval

## Overview

发布一个需求前做两件事：

1. 按团队模板生成审批邮件 `.eml`（收件人/主题预填，双击即可在邮件客户端预览并发送——**发送动作始终由用户完成，绝不代替发送**）。
2. 在 Confluence database「System Change Log」(id `376700933`，PRODTECH 空间) 创建一行发布记录。

Step 0：以 harness 加载本技能时给出的 base directory 为 `$SKILL_DIR`（若该路径是 symlink，用 `readlink -f` 解析真实路径再拼接 scripts/config 路径）；本仓库注册路径为 `/Users/yangjun/Desktop/my-ai/.agents/skills/release-approval`。

## 配置（模板入库、实配置本地、缺失静默回退）

- `config.template.json`：入库的模板，含占位默认值。
- `config.json`：本地实配置（已被 `.gitignore` 忽略），**存在则优先生效**；不存在或某键缺失时回退模板对应值，不要报错。
- 读取方式：`node -e "const c=require('$SKILL_DIR/config.json')" 2>/dev/null || node -e "const c=require('$SKILL_DIR/config.template.json')"`，逐键合并。

关键配置键：

- `email.to` / `email.cc` / `email.from`：固定收件人。**to 为空时先问用户本次收件人**，用户给出后顺手写入 `config.json`（下次免问）。
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
4. 可选 `open <eml路径>` 让用户在邮件客户端预览正文；不自动发送。

## 第 3 步：System Change Log 创建发布记录行

背景（勿重试已排除的路由）：官方公开 API 无 database 行级操作（CONFCLOUD-77328 open，`/items` 路由 404）；database 前端是 sandbox iframe 独立应用，browser-use 的 snapshot/click/脚本注入/网络捕获均无法触达。因此行创建走 **computer-use 屏幕级自动化**，等效人工操作。

1. **schema 采集（仅 `database.columns` 为空时）**：请用户打开 Qoder 应用内浏览器窗口，用 browser-use navigate 到 `database.url`，`take_screenshot` 视觉读取全部列名，把「列名 → 填充值来源」映射写入 `config.json` 的 `database.columns`（值用字段名或固定文案占位，如 `"Release item": "name"`）。之后每次免采集。
2. **打开页面**：browser-use navigate 到 `database.url`；先 `take_screenshot`，若报 `NATIVE_BROWSER_VIEWPORT_UNAVAILABLE` 则请用户打开应用内浏览器窗口后重试；若页面跳到 id.atlassian.com 登录页则请用户在受控窗口重新登录。
3. **录入**：用 Skill 工具调 computer-use（屏幕级），视觉定位行新增入口（表格底部 `+` / "New entry" / 末行空行），逐格填入按 `database.columns` 映射的值；人名/mention 类列直接输入姓名文本。
4. **验证**：截图确认新行内容无误。失败重试一次；仍失败走兜底——把按列组织的记录内容完整输出到对话，`open` database 页面让用户手动粘贴，汇报中标注「行创建：手动」。
5. 测试产生的行要清理时，同样用 computer-use 定位该行删除。

## 第 4 步：汇报

- eml：绝对路径 + 主题 + 收件人（等用户自行发送）。
- 行：computer-use 成功（附验证截图已确认）或手动兜底。

## Resources

- `scripts/build-eml.mjs`：字段 JSON → RFC822 `.eml`（HTML 三列表格正文，✅/`\` 状态列，主题 RFC2047 编码）。缺 name/prUrl/reviewer/to 时 exit 1。
- `config.template.json` / `config.json`：见「配置」。
