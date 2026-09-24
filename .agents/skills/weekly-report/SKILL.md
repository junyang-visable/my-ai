---
name: weekly-report
description: 起草并保真更新 Eric(Jun Yang) 的 Confluence 周报页(pageId 69632024)。Use when 用户提到 周报、weekly update、CWn、汇总本周/过去一周工作、更新周报页面。收集 Jira/git/Confluence/Obsidian 一周动态，按 CWn 模板起草，用户确认后 HTML 往返方式更新页面并做归一化校验。
---

# Weekly Report

## Overview

为 Jun Yang(Eric) 维护 Confluence 周报页 [Weekly update - Eric](https://visable.atlassian.net/wiki/spaces/~712020b71ea144f4734a7895e66e51861d7dc3/pages/69632024)：pageId `69632024`，cloudId `visable.atlassian.net`，Atlassian 账号 `712020:75c2285d-8115-445a-8b9d-c5244bebf36f`（jun.yang@visable.com）。每周新增一期 `CWn` 置顶；历史期数永不改动。期数 = ISO 周号（如 2026-09-23 → CW38）。

流程：收集 → 起草 → 用户确认 → 更新与校验。前两步只读；未获确认绝不调用 `updateConfluencePage`。

## 1. 收集（过去一周）

写草稿前先与用户确认时间窗口（如 9.16–9.23）。四个来源并行查询：

1. **Jira**（atlassian MCP `searchJiraIssuesUsingJql`）：
   JQL `assignee = currentUser() AND updated >= "<窗口起始日>" ORDER BY updated DESC`，fields 只取 summary/status/issuetype/project/updated。结果常超 25k tokens 被落盘——用 Grep 在落盘文件中按行号对齐 `"key"`/`"summary"`/`"name"`(status)/`"updated"` 四类行还原每张票。
2. **Git**：`bash /Users/yangjun/Desktop/my-ai/.agents/skills/weekly-report/scripts/scan_git.sh <YYYY-MM-DD>`。扫 ~/Desktop/project、~/Desktop/my-ai、~/Documents 一级子仓库（`--all --since`），默认 author "Jun Yang"；`--all-authors` 或追加目录参数可扩展。Obsidian Vault 的日记提交也会被扫到，注意区分。
3. **Confluence**（`searchConfluenceUsingCql`）：`contributor = currentUser() AND lastmodified >= "<窗口起始日>" AND type = page ORDER BY lastmodified DESC`。
4. **Obsidian 日记**：`~/Documents/Obsidian Vault/10-Daily/YYYY-MM-DD.md`。会议、1v1、竞品调研、非代码工作的唯一来源，git/Jira 查不到。

## 2. 起草

页面结构：`# CWn` → `# Business projects` 表 → `# Tech OKR Projects` 表 →（历史期数原样保留，新期置顶）。

表格骨架（列宽与表头底色保持一致）：

- Business projects：th 加 `data-background="#f0f1f2"` 与 `style="background-color: #f0f1f2"`，data-colwidth 依次 106/126/222/107/194，table `data-width="760"`。GTM 域的 Account Creation 与 BV verification 两行共用首列 `rowspan="2"`。Jira ticket 列用带文字的 `<a href="https://...pageId/标题slug">标题</a>`（slug 可省，服务端会规范化）。
- Tech OKR Projects：data-colwidth 166/363/226；Status 列多事项用 `<ul><li><p>`。

条目写作风格（用户 2026-09-23 手工修订 CW38 后确立，必须遵守）：

- 不写 Jira 工单号与状态标注（如"（FE-1117 Done）"）——票号在 Jira 可查。
- 不写实现层细节（如"ODPS SQL 分区约束""模块级 event bus"）——只写"做了什么 + 结果"。
- 微优化不单列一条（并入或删掉）。
- Status 列放已完成的落地动作（含推广落地，如"团队内推广巡检"）；Comment 列的 Next step 只留真正未做的，两栏不重复。
- 沿用既有词汇：巡检、沉淀排查方案。条目用中文，表头英文。

Release date 列沿用上期同项目的排期写法（`- 9.7开发 - 9.11联调` 式的 `<ul><li>`），有变更时按用户口径更新（如发布改期）。

草稿以对话内 Markdown 表格完整展示给用户，等确认后再进入第 3 步。

## 3. 确认

未获用户明确确认不得写页面。注意：auto 模式下确认分类器可能不采信 AskUserQuestion 的选项结果——若被拦截，请用户直接在对话里打字确认（如"确认更新"），收到后原样执行准备好的更新调用，不要临时改动内容。

## 4. 更新与校验

1. `getConfluencePage`（contentFormat=html）取当前全文；大响应会落盘，工具返回里有文件路径。
2. 把新期 HTML（`<h1>CWn</h1>` 到 Tech OKR 表 `</table>`）存为独立文件，然后：
   `node /Users/yangjun/Desktop/my-ai/.agents/skills/weekly-report/scripts/confluence_body.mjs prepare <fetched路径> <new-section.html> /tmp/<cwn>_body.html /tmp/<cwn>_wrapped.txt`
   产物 = 新期 + 旧全文（已剥 data-local-id；wrapped 版在 `><` 边界插换行，便于分段 Read 与转写）。fetched 原文同时就是回滚备份。
3. 分段 Read wrapped 文件，把全文作为 `body` 调 `updateConfluencePage`：contentFormat=html、includeBody=false、versionMessage="Add CWn weekly update"。新期节点不写 data-local-id（转换器自动生成）。
4. 校验：重新 `getConfluencePage`（html，落盘），运行
   `node /Users/yangjun/Desktop/my-ai/.agents/skills/weekly-report/scripts/confluence_body.mjs verify <新fetched路径> /tmp/<cwn>_body.html`
   `equal: true` 即通过。脚本已忽略两类服务端无害规范化：wiki 链接去掉标题 slug（pageId 保留、锚文本不变）、rowspan/data-colwidth 属性重排。出现其他 hunk = 内容损坏，立即用备份回滚。
5. 已知必须存活的锚点：CW23 表格里的 inline comment（`data-annotation-id="3e0942ae-b10c-4c28-93a0-564510561f21"`，两处 span）。校验通过后向用户汇报新版本号与结论。

## 回滚

第 2 步的 fetched 原文即更新前快照；回滚 = 把它原样作为 body 重新 `updateConfluencePage`。

## Resources

- `scripts/scan_git.sh` — 多仓库 git 提交扫描（author 过滤、ISO 日期入参）
- `scripts/confluence_body.mjs` — `prepare`（新期拼接 + local-id 剥离 + 换行包裹）与 `verify`（归一化比对，忽略已知服务端规范化）
