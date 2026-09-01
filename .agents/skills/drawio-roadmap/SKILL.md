---
name: drawio-roadmap
description: 画甘特式项目排期 Roadmap 图（drawio）。沉淀时间轴网格、任务条/里程碑、阶段配色体系、坐标公式与验证工作流，坐标断言与渲染验证 harness 均内置，自包含无外部技能依赖。Use when user mentions roadmap、排期图、甘特图、项目计划图、迭代日历、roadmap 图、画排期、Nexus 排期, or asks to create/adjust a timeline-based schedule diagram in drawio.
---

# 甘特式 Roadmap 排期图（drawio）

标准产出参考：`docs/nexus/ROADMAP.drawio`（Nexus 排期图，v0.9）。用户排期数据以 ROADMAP.md 为 source of truth，drawio 为可视化衍生；改排期需两处同步 + 版本号升级 + 更新记录。

## 坐标体系（唯一需要背的公式）

```
DAY_W = 14          # 每天格宽固定 14px
x(日期) = X0 + days_since_start × 14
```

- `X0` = 时间轴第一天的 x（日期格首列左缘）
- 网格行高 32px（首行 y=158 起），任务条 height=20、y=行y+6；菱形 16×16、y=行y+7
- 关键纵向基准（Nexus 值）：图例 y=62 / 月表头 y=104 h=22 / 星期行 y=126 h=16 / 日期行 y=142 h=16 / 首行 y=158
- **改时间轴起点**（如 8.24 起）：列数变化 = ±N 天 → 9/10 月所有元素 x ∓ N×14；表头/行背景/图例容器宽度随之增减；**必须同步重算周末背景列**（原周末位置变成工作日）

### 元素对位规则（自检）

| 元素 | x 规则 |
|---|---|
| 区间条（开发/联调） | x = x(起日)，width = 天数×14，左缘对齐首日格左缘 |
| 里程碑菱形 | x = x(当日) − 1，即水平居中于当日格中心 |
| 月分隔线（edge） | x = x(当月 1 日) |
| 今天线（虚线 edge） | x = x(今天)，配红字标签居中于线上 |
| 跨度条（如存量修复整月） | x = x(起日)，width 到末日晚 |

## 布局结构（上→下）

```
标题 (fontSize=20) + 副标题 (排期摘要一行 · v版本号)
图例虚线框：阶段色样 + 说明文字，每组 155px，容器宽=行背景宽
表头：左「条目/阶段」深灰块 + 月份蓝条 (#1565C0 白字)，月条宽=当月天数×14
日期网格：星期行 + 日期行，周末格底色 #ECEFF1/#F5F5F5 字色 #B0BEC5，工作日白底 #666666
行背景：每行白/#FBFBFB 交替，宽度=时间轴总宽
周末背景列：#EFEFEF 无边框，y=首行y，height=全部行总高
项目分组区：左列项目名色块（归属色，跨该组行高）+ 阶段白底标签
甘特区：任务条/菱形 + 右侧灰字说明 (fontSize=8, #666666)
页脚：待确认事项 + 版本号 · 更新日期 · 数据源
```

## 阶段配色（v0.9 起，跨项目统一）

**核心原则：颜色只表达阶段，不表达项目。** 项目归属由左侧项目名色块表达。新增任务条禁止套用项目色。

| 阶段 | 形状 | fillColor | strokeColor | fontColor |
|---|---|---|---|---|
| 开发 | 胶囊 rounded=1;arcSize=30 | #dae8fc | #6c8ebf | #1565C0 |
| 联调 | 胶囊 | #ffe6cc | #e69138 | #E65100 |
| 提测 | 菱形 | #d6b656 | #d6b656 | — |
| UAT | 菱形 | #9673a6 | #9673a6 | — |
| Release | 菱形 | #b85450 | #b85450 | — |
| 存量修复（示意） | 胶囊 | #d5e8d4 | #82b366 | #2E7D32 |
| 周末背景 | 矩形 | #EFEFEF | none | — |

左侧阶段标签字体色呼应菱形色：提测 #A67C00 / UAT #7B1FA2 / Release #B71C1C。

## 新建 roadmap 工作流

1. **定时间轴**：起止日期 → X0、总天数、右缘 = X0 + 总天数×14；工作日/周末星期行用 `date` 命令校验（如 2026-09-13 → 周日）
2. **生成网格**：先写星期/日期双行（ID 按月份分段：8 月 c66-c81、9 月 c82-c141、10 月 c142-c203），再写周末列、行背景、表头
3. **铺任务**：每个项目一组（项目名色块 + 阶段标签 + 甘特元素），对位规则见上表；每个区间条和菱形都带阶段文字
4. **图例**：按阶段配色表逐项配样（含形状差异：胶囊 vs 菱形），图例项数与图内实际形状种类一一对应
5. **文本层**：副标题排期摘要、待确认事项、页脚版本号

> 大批量网格生成（60+ cell）推荐脚本生成（Python 拼字符串）：一次成文、坐标零漂移；SearchReplace 手改易超 token 限制且逐行出错。

## 修改 roadmap 工作流

常见变更 → 操作：
- **新增任务条**：套用阶段色（非项目色）；x 用坐标公式；同步副标题/待确认事项/页脚版本
- **改排期日期**：任务条 x/width 重算；菱形 −1 规则别忘
- **时间轴整体平移**（如 8 月从 24 号起）：见「坐标体系」末段；批量平移用脚本（id→平移量映射表），用 `xml.etree.ElementTree` 解析后断言变更数
- **搜历史排期**：更新记录表是变更审计线索，新增变更必须追加行

## 验证工作流（程序化断言，禁止只看截图）

1. **坐标断言**（内置脚本，直接执行）：
   ```bash
   python3 .agents/skills/drawio-roadmap/scripts/verify_roadmap.py docs/nexus/ROADMAP.drawio 2026-08-24
   # 参数：drawio 路径 + 时间轴首日；输出 PASS/FAIL
   ```
   自动断言：日期序列完整且 gap=14、月表头宽=轴内天数×14（含截断月）、周末列与周末日期格一一对应、无元素超出右缘。
   任务条/菱形对位（公式 + 菱形 −1）因每次任务不同，按「元素对位规则」表逐个补断言（Python + ElementTree）。
2. **渲染验证**（harness 内置于本技能 `scripts/`）：
   ```bash
   # server 未运行时先启动（8123 端口，须从工作区根启动）：
   python3 .agents/skills/drawio-roadmap/scripts/cors_server.py
   # 工作区根准备 tmp 文件（验证页固定 fetch /tmp-verify.drawio）：
   cp docs/nexus/ROADMAP.drawio tmp-verify.drawio
   # 浏览器打开：
   # http://127.0.0.1:8123/.agents/skills/drawio-roadmap/scripts/drawio-verify.html
   ```
   验证页自动 encodeURIComponent → deflate-raw → base64 → viewer.diagrams.net/#R iframe 渲染；用 Chrome MCP `wait_for` 关键文本 + 截图做最终人工确认，坐标断言已兜底。禁止经 Chrome MCP 的 URL/evaluate_script 传 base64 长串（会静默损坏字符，宿主页自己 fetch 才安全）
3. **md 同步检查**：版本号、排期数据、更新记录三处与 md 一致

## 自检清单

- [ ] 每个任务条/菱形都带阶段文字（历史坑：WhatsApp 联调条 value 空串，v0.6 起漏到 v0.9 才发现）
- [ ] 新增条颜色套阶段色而非项目色
- [ ] 菱形 −1、区间条左缘对齐两条对位规则全图一致（历史坑：GTM 菱形曾左缘对齐差 7px）
- [ ] 周末背景列与日期网格 weekend 标记一一对应
- [ ] 副标题摘要、图例、md 更新记录、版本号四处同步
- [ ] 里程碑日期星期正确（用 date 命令验证）
- [ ] 渲染验证：无“URI malformed”弹窗（#R URL 须 encodeURIComponent→deflate-raw→base64，由验证页自带）

## 复用资产（全部内置于本技能或本仓库）

| 资产 | 位置 | 用途 |
|---|---|---|
| 标准产出 | `docs/nexus/ROADMAP.drawio`（本仓库示例） | 抄结构/样式/坐标的直接参照 |
| 数据源 | `docs/nexus/ROADMAP.md` | 排期 source of truth |
| 坐标断言脚本 | `scripts/verify_roadmap.py`（内置） | 网格/表头/周末列/右缘四项断言 |
| 渲染 CORS server | `scripts/cors_server.py`（内置） | 8123 端口，从工作区根启动 |
| 渲染验证页 | `scripts/drawio-verify.html`（内置） | fetch tmp → viewer iframe 渲染 |

## 自包含

坐标断言与渲染验证 harness 均内置 `scripts/`，阶段配色专有于本技能——甘特式排期图全流程自包含，无其他技能依赖。
