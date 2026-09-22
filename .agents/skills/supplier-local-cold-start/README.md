# Supplier Local Cold Start

自动化本地 staging 环境启动：安装依赖 → 获取登录态 → 起 dev server → 注入 cookie → 打开浏览器。

## 安装

解压到你所用 IDE 的 skill 目录（全局或项目内均可）。脚本用相对路径引用，位置不限。

## 一次性配置

在 `~/.zshrc` 中添加：

```bash
export STAGING_EMAIL="your-email@visable.com"
export STAGING_PASSWORD="your-password"   # visable 邮箱不需要
export GITHUB_TOKEN="ghp_xxxx"
```

确保 `~/.npmrc` 包含：

```
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

执行 `source ~/.zshrc` 生效。

## 使用

在项目目录下对 agent 说：

> 启动本地 staging，supplier-id 是 xxx

或直接调用：

```bash
bash scripts/run.sh bootstrap.py --supplier-id=<supplier-id>
```

查询当前运行中的 dev server（任意目录可跑，只读）：

```bash
bash scripts/run.sh bootstrap.py --status
```

依赖疑似陈旧时强制重装（lockfile 变更会自动触发重装）：

```bash
bash scripts/run.sh bootstrap.py --supplier-id=<supplier-id> --reinstall
```

首次使用 visable 邮箱会弹浏览器完成微软 SSO，之后全程静默。

## 支持项目

- business-insights-frontend
- supplier-onboarding-frontend
- visitors-frontend
- ad-center-frontend
- product-editor-frontend
- customer-dashboard-frontend

## 注意事项

- 多项目可并行运行，端口从 3000 起自动分配
- 重新启动同项目会自动清理上次进程
- 热更新正常工作，改代码保存即生效
- Python 依赖：优先复用系统已有 playwright，没有才建专属 venv（`~/.config/supplier-local-cold-start/venv/`）
- 状态数据（session 缓存 / SSO profile / 凭据 / debug 截图）在 `~/.config/staging-local-dev/`，不会被系统清理；旧版放在 /tmp 的数据首次运行会自动迁移
- dev server 进程记录与日志在 `/tmp/`（`dev-pids-<project>.json`、`staging-local-dev-<project>.log`），重启自动失效

## 文件结构

```
supplier-local-cold-start/
├── SKILL.md          # agent 指令
├── projects.json     # 项目配置
├── projects.md       # 项目差异速览
├── README.md         # 本文档
└── scripts/
    ├── bootstrap.py     # 主入口（含 --status / --reinstall）
    ├── common.py        # 共享常量与工具（路径单源）
    ├── session.py       # 登录态获取
    ├── open_browser.py  # cookie 注入 + 打开浏览器
    ├── view_page.py     # 页面检视（fast + 交互）
    ├── setup.sh         # 依赖安装
    └── run.sh           # venv python 入口
```
