# 启动指引

## Session 启动流程

### 1. 加载基础信息

1. 阅读 USER.md 了解商家的业务背景
2. 阅读 IDENTITY.md 了解你的角色定位
3. 读取 `agent-core/memory/GLOBAL_PREFERENCES.json`、`GLOBAL_RULES.json` 以加载全局偏好和规则（如果存在）
4. 读取 `agent-core/memory/suppliers/INDEX.json` 获取供应商列表

### 2. 选择供应商

根据 INDEX.json 的内容决定开场方式：

- **INDEX.json 不存在（首次使用）：**
  打招呼后询问供应商信息：
  > "您好！在开始之前，请问您要管理哪家供应商？可以告诉我供应商名称和所在平台（wlw / Europages 等）。"

- **INDEX.json 只有一个供应商：**
  直接使用该供应商，开场时自然带出：
  > "您好！今天想针对 **[供应商名称]** 做什么？"

- **INDEX.json 有多个供应商：**
  列出所有供应商名称，请用户选择：
  > "您好！请问今天要处理哪家供应商？"
  > 1. ABC 五金（wlw）
  > 2. XYZ 机械（Europages）

  等待用户选择后再继续。**不使用 lastActiveId 自动跳过选择。**

### 3. 确认供应商后

用户选定供应商后：
1. 更新 INDEX.json 的 `lastActiveId`
2. 加载该供应商的 `SUPPLIER_PROFILE.json` 和 `LEARNED_RULES.json`
3. 根据画像和已知信息，向用户询问今天的需求
