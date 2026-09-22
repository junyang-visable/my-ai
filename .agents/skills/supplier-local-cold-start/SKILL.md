---
name: supplier-local-cold-start
description: >-
  Fully automates silent local staging-backed dev for supplier-onboarding,
  business-insights, visitors, ad-center, product-editor, and customer-dashboard.
  Agent pre-installs deps once (reuses system playwright if present, else isolated
  venv), picks a free port (3000+), starts dev server, silently obtains the staging
  _user_session (cached; password login by default, visable accounts fall back to
  Microsoft SSO), injects cookie into the browser,
  and opens the app. Credentials read from STAGING_EMAIL / STAGING_PASSWORD env vars.
  User only provides supplier-id. Use for /supplier-local-cold-start or localhost
  staging auth setup.
---

# Supplier Local Cold Start（全自动 · 静默）

全程静默：agent 直接把本地 dev server 起来并打开业务页。凭据（邮箱/密码）从环境变量 `STAGING_EMAIL` / `STAGING_PASSWORD` 读取，运行时不交互询问。

> **agent 注意**：直接跑 `bootstrap.py` 即可。**不要**自己定位 yarn/node、**不要**检查 node 版本、**不要**单独跑 `yarn dev` —— bootstrap 内部已解析 node/yarn 路径、自动选空闲端口、清理上次 dev server。自行介入只会触发"yarn 不在 PATH，正在定位"的重复开销。

> 默认走邮箱+密码登录（凭据从环境变量读取）。@visable.com 邮箱无密码，自动回退到微软 SSO（首次需开一次可见浏览器）。

## Agent 工作流

> **项目识别**：必须在**项目根目录**（含 package.json）跑。bootstrap 用 cwd 名匹配 `projects.json` key（如 `business-insights-frontend`）。agent 先 `cd` 到项目根再跑（项目路径因人而异，skill 不猜路径）。若 cwd 名与 key 不同但确在该项目根，可用 `--project=<name>` 指定配置名（仍需在该项目根目录）。cwd 不是项目根会报错并列出已知项目。

> **不要自己查环境变量**：IDE agent 是非交互 shell，不加载 `~/.zshrc`，你 `echo $STAGING_EMAIL` 会显示空——这是误报。`run.sh` 内部已从 `.zshrc` 读 `STAGING_EMAIL`/`STAGING_PASSWORD`/`GITHUB_TOKEN` 传给 bootstrap。**别重复诊断、别提示用户配置**，只管跑 `run.sh bootstrap.py`，按 `NEED_EMAIL`/`NEED_PASSWORD` exit code 处理即可。

### 0. 预装依赖（自动，无需手动）

**不要自己查 marker、不要单独跑 setup**。`run.sh` 内部会检测 python+playwright，缺失才自动跑 setup（一次性，marker 落在 `~/.config/supplier-local-cold-start/.installed`，复用系统 python 时秒过）。直接执行第 3 步的 `bash scripts/run.sh bootstrap.py ...` 即可。

> **必须用完整文件权限运行（非沙箱）**：登录和页面检视用 `channel="chrome"` 启动系统 Chrome（`/Applications/Google Chrome`），沙箱会拦截启动；而 chromium 二进制下载被公司代理（云壳）拦截 `cdn.playwright.dev`，没有 fallback。所以**沙箱模式必然失败**，agent 首次运行就请用完整权限，别等失败再重试。

### 1. 收集 supplier-id

- 消息里已有 → 直接用
- 没有 → 用**普通文本**问用户 supplier-id（自由文本输入，**不要用选项/多选问答**）

### 2. 端口（自动）

bootstrap 自动从 3000 起选第一个**空闲**端口（被占就顺延），并按记录的进程组精确清理**上次自己起的** dev server（不碰别的进程）。agent/用户无需关心端口。

### 3. 一键启动（静默获取登录态）

```bash
bash scripts/run.sh bootstrap.py \
  --supplier-id=<supplier-id>
```

凭据从环境变量读取，agent 无需传 `--email`/`--password`。退出信号处理：

| 退出信号 | 含义 | Agent 动作 |
|----------|------|-----------|
| `NEED_EMAIL` (exit 2) | 环境变量无 `STAGING_EMAIL` | 提示用户在 `~/.zshrc` 配 `export STAGING_EMAIL=…`（非 visable 邮箱还需 `STAGING_PASSWORD`）后重跑 |
| `NEED_PASSWORD` (exit 3) | 非 visable 邮箱缺密码 | 提示用户在 `~/.zshrc` 配 `export STAGING_PASSWORD=…` 后重跑 |
| 成功 | dev server 已起、页面已开 | 汇报 URL（注意是 bootstrap 实际选用的端口，不一定是 3000） |

> **不要把密码放在命令行的 `--password=` 里**：会因「命令行携带明文密码」被拦下。统一走环境变量。

> **超时预算**：暖启动（依赖已装、dev server 可复用、session 有效）秒级返回；冷启动（装依赖 + 构建 + 登录）可能 5-10 分钟（本机 npm registry 限速）。agent 调用时给足超时（≥10 分钟）或用后台运行；install 期间脚本每 30s 打一行心跳，属正常非卡死。

凭据只从环境变量 `STAGING_EMAIL` / `STAGING_PASSWORD` 读取。缺邮箱 → `NEED_EMAIL` 报错；非 visable 邮箱缺密码 → `NEED_PASSWORD` 报错。提示用户在 `~/.zshrc` 配好后重跑，**不要交互询问、不要写凭据文件**。

### 4. 汇报 URL

bootstrap 输出 JSON 里的 `url` 字段就是实际地址（端口可能是 3000/3001/…）。把它报给用户。

页面打开方式：起一个一次性本地 HTTP 服务，访问时通过 `Set-Cookie` 把 `_user_session` 写进用户**自己的浏览器**（localhost cookie 跨端口共享），再 302 跳业务页。**不用 Playwright 窗口**。该服务生命周期跟随 dev server（dev server 停则自动退）。

### 5. 检视运行中的页面（agent 自己要看时）

**重要**：bootstrap 只负责起 dev server + 打开页面。agent 自己想看页面内容时，**不要重跑 bootstrap**（那会重启 dev server）。

用检视脚本，用缓存的 `_user_session` 渲染运行中的页面，不动 dev server：

```bash
# 快速读 SSR 文本（毫秒级，适合 Nuxt 项目）
bash scripts/run.sh view_page.py <url> --fast
# Playwright 渲染（支持交互）
bash scripts/run.sh view_page.py <url>
# 点击后再读
bash scripts/run.sh view_page.py <url> --click "button.submit"
# 存整页截图
bash scripts/run.sh view_page.py <url> --screenshot /tmp/page.png
```

`<url>` 用 bootstrap 输出的业务页地址。前提：dev server 在跑、`~/.config/staging-local-dev/session` 有缓存。

### 6. 查询运行中的 dev server

新会话或上下文压缩后，想知道哪些项目在跑、端口各是多少（任意目录可跑，只读）：

```bash
bash scripts/run.sh bootstrap.py --status
```

输出 JSON：各项目的端口、业务页 URL、存活状态、日志路径、cookie 注入入口。

## 静默与缓存机制

- `_user_session` → `~/.config/staging-local-dev/session`（命中后连浏览器都不启动）
- 凭据 → 环境变量 `STAGING_EMAIL` / `STAGING_PASSWORD`
- 微软会话 cookie → `~/.config/staging-local-dev/playwright-profile`（仅 visable SSO 用）
- 登录失败落盘 `~/.config/staging-local-dev/debug/*.png` + `*.url`
- venv 与安装 marker → `~/.config/supplier-local-cold-start/`（/tmp 会被系统定期清理，放那里会意外触发重装）
- dev server 进程记录与日志 → `/tmp/dev-pids-<project>.json`、`/tmp/staging-local-dev-<project>.log`（运行时状态，重启自清）

## 两层过期

| 会话 | 周期 | 过期时 |
|------|------|--------|
| `_user_session`（wlw 应用） | 短 | headless 自动用微软会话续期，静默 |
| 微软 SSO 会话 | 长 | headless 续期失败 → visable 自动开浏览器重新登录一次 |

## 登录流程（内部）

registration 页 → `press_sequentially` 输入邮箱 → Continue → 跳 `/en/login?flow=` → 输入密码 → JS `el.click()` 点 Log in（绕过 CookieScript 横幅）→ 抓 `_user_session`。@visable.com 邮箱无密码，走微软 SSO。

调试 DOM：`bash scripts/run.sh session.py --headed --refresh`

## 排错

| 现象 | 处理 |
|------|------|
| playwright 未装 | 跑 `bash scripts/setup.sh` |
| 端口 3000-3020 全被占 | 关掉其中无关进程 |
| NEED_EMAIL | 提示用户配置 `STAGING_EMAIL` 环境变量 |
| NEED_PASSWORD | 提示用户配置 `STAGING_PASSWORD` 环境变量 |
| `/me` 401 | 删 `~/.config/staging-local-dev/session` 后重跑（自动续期） |
| 续期失败 | 看 `~/.config/staging-local-dev/debug/`，必要时 `session.py --headed` 手动确认 |
| dev server 起不来 / 等端口超时 | 看 `/tmp/staging-local-dev-<project>.log`（超时时 bootstrap 会自动附日志尾部） |
| 依赖疑似陈旧 | lockfile 变更会自动重装；node_modules 存在但损坏时加 `--reinstall` 强制重装 |

## 项目配置

[projects.json](projects.json) · [projects.md](projects.md)
