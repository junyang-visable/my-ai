# MCP 工具接入指南

在 Cursor 中接入 MCP（Model Context Protocol）可让 AI 安全地调用浏览器调试、本地文件等能力。本指南列出推荐组合及配置方式。

## 推荐接入的 MCP 工具

| MCP | 用途 | 说明 |
|-----|------|------|
| 浏览器 DevTools MCP | 页面元素、网络、控制台等调试上下文 | 与 Chrome / Chromium DevTools 协议对接，便于 AI 理解运行时行为；适合排查样式、请求与前端错误。 |
| 文件系统 MCP | 受控读写工作区文件 | 在允许的路径内列出、读取、搜索文件，补充编辑器上下文；注意将根路径限制在项目目录。 |

> 具体包名与启动命令以各 MCP 官方文档为准；团队可统一固定版本号以便复现环境。

## 配置方式

1. 打开 **Cursor** → **Settings**（设置）。
2. 进入 **Features** → **MCP**（或当前版本中与 MCP 相关的配置入口）。
3. 使用 **Edit in settings.json** 或界面提供的 JSON 编辑能力，在 MCP 配置中加入服务器定义。

### `mcp.json` 示例（项目级）

若团队使用项目根目录下的 `.cursor/mcp.json`（或 Cursor 文档中约定的项目 MCP 配置文件），可参考以下结构；**请将路径、命令与参数替换为实际环境**。

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "[替换: @your-org/chrome-devtools-mcp 或官方包名]"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "[替换: 绝对路径，例如 /path/to/your/vue-nuxt-repo]"
      ]
    }
  }
}
```

### 用户级配置说明

- 用户级 MCP 配置通常位于 Cursor 的用户设置目录，与项目级配置可同时存在；**优先以团队文档为准**，避免重复注册同名 server。
- `filesystem` 的最后一个参数必须是**本机绝对路径**，且仅包含允许 AI 访问的仓库根目录，不要使用 `$HOME` 整目录作为根。
- 若使用 `npx`，首次运行会下载包；内网环境可改为 `node` 直接执行本地已安装的 CLI。

## @docs 索引配置

为让 AI 优先引用官方与团队文档，建议在 Cursor 的 **Docs** / **Indexing**（或当前版本的文档索引功能）中加入以下索引；UI 库条目请替换为项目实际使用的库。

| 名称 | 说明 | 建议索引来源 |
|------|------|----------------|
| Vue 3 | 组合式 API、`<script setup>`、类型 | https://vuejs.org/ |
| Nuxt 3 | 路由、数据获取、SSR | https://nuxt.com/docs |
| Pinia | Store、action、TypeScript | https://pinia.vuejs.org/ |
| [替换: UI 库名称] | 组件 API 与主题 | [替换: 例如 https://element-plus.org/ 或内部 Storybook URL] |

配置完成后，在对话中可通过 `@Vue`、`@Nuxt` 等（以 Cursor 实际支持的 doc 别名为准）引用文档，减少幻觉 API。

## 安全与合规提示

- 仅向 MCP 暴露必要的目录；不要将含密钥、`.env` 生产配置的父目录整块挂载给 filesystem MCP，除非流程已审计。
- DevTools MCP 会接触页面与网络信息，**勿在含敏感数据的未脱敏环境**中默认开启；按环境区分配置。
