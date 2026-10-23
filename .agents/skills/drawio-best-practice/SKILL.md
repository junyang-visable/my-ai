---
name: drawio-best-practice
description: 画易读易懂的 drawio 图的方法论。支持 MD 文档自动转 drawio。Use when user mentions drawio、画图、架构图、流程图、矩阵图、对比图、决策树、应急预案图、监控全景图、draw.io、画个图出来、转drawio、生成drawio、md转图.
---

# Drawio 最佳实践 — 最小成本画出阅读成本最低的图

## 核心原则

**一张好图 = 3 秒抓住结构 + 30 秒看懂细节。**

做到这一点只需要三件事：
1. **选对图类型**（决策树 vs 表格 vs 流程）
2. **用对 drawio 元素**（原生形状 + HTML 表格，不用 markdown）
3. **颜色只做一件事**（区分归属 OR 区分优先级，不能同时两种语义）

## 标准工作流

```
选图类型 → 按需读参考 → 生成 XML → 校验（0 error）→ 导出 PNG 预览 → 视觉检查 → 交付
```

**校验和预览是硬门槛：没跑校验、没看过渲染图的图不算完成。**

### Step 0: 输入是 MD 文档时，先分析结构

读取 MD 文档，识别信息类型：

| MD 中的结构 | 映射为 drawio 图类型 |
|------------|---------------------|
| `# 标题` + `## 子标题` | drawio 的 Part 章节（深色标题条） |
| markdown 表格 `\|...\|` | HTML `<table>`（直接转换，加颜色行） |
| 有序列表 `1. 2. 3.` | 并排 SOP 步骤框（矩形 + 箭头） |
| 条件判断 "如果...则..." | 决策树（菱形 + 矩形） |
| 分类/分组 `### 类别A` | 分区卡片或表格分组行 |
| 优先级标记 P0/P1/P2 | 颜色编码（红/黄/绿） |
| 链接 `[text](url)` | 表格外 UserObject；表格内 `<a href>`（见 `references/links.md`） |
| 指标/数据 | 数值直接填入表格单元格 |

### Step 1: 选图类型

拿到需求后第一个问题：**这个信息适合用什么结构展示？**

| 信息类型 | 用什么 | 不用什么 |
|---------|--------|---------|
| **是/否判断链** | 决策树（菱形+矩形） | 表格 |
| **多步骤操作** | 并排矩形 + 箭头 | 纯文字列表 |
| **多维度对比** | HTML `<table>` | markdown 表格 / shape=table |
| **指标矩阵** | HTML `<table>` + 颜色行 | 一堆小方块 |
| **全景/拓扑** | 分层布局 + 归属颜色 | 所有东西挤一层 |
| **升级路径** | 横向节点 + 箭头 | 纯文字 |
| **场景速查** | HTML `<table>` 带颜色行 | 每个场景一个大框 |

各图型的成熟结构示例见 `references/examples.md`。

**关键决策：表格 vs 图形？**
- 信息是"分类列表" → **表格**（阅读成本最低）
- 信息有"流向/因果/顺序" → **图形**（箭头表达关系）
- 两者都有 → **混合**（上半部分决策树，下半部分表格）

### Step 2: 按需读参考（生成前必读对应项）

| 情况 | 读 | 何时必读 |
|------|-----|---------|
| 要给任何元素上色 | `references/color-cards.md` | 每次生成/改色前 |
| 图里要放表格 | `references/html-tables.md` | 生成前**必读**（列宽/高度是最常见的坑） |
| 图里有可点击链接 | `references/links.md` | 含 Jira/监控/报表链接时 |
| 想参考同类图的成熟结构 | `references/examples.md` | 布局拿不准时 |
| 校验报错 / 预览异常 | `references/troubleshooting.md` | 排查时 |

### Step 3: 生成 XML 并校验

1. 从下方「最小可运行骨架」复制起点，按选定的图型和色卡规范写 XML，`Write` 输出 `.drawio` 文件
2. **必跑校验**：

```bash
python3 .agents/skills/drawio-best-practice/scripts/validate_drawio.py <file>.drawio
```

3. **error 必须清零才算过**；warning（pageHeight 溢出、表格列宽疑似溢出）逐条确认

校验器负责（机器可查）：XML 解析、mxfile/diagram/root 结构、保留节点、**页内 id 重复**、parent/source/target 悬空引用、vertex 缺几何/宽高、edge 缺端点（浮动连线豁免）、value 含 HTML 却缺 `html=1`、`shape=table` 禁忌、value 里写 markdown 表格。

校验器不管（人工/预览管）：视觉布局、y 重叠、连线走向、可读性；style 尾分号、自闭合标签空格等 drawio 本身兼容的写法也不查。

**修改已有 `.drawio`**：整读文件 → 认准唯一 `id` 锚点 `Edit` → 重跑校验 → 重跑预览。

**校验脚本自身改动后**：跑 `python3 .agents/skills/drawio-best-practice/scripts/test_validate_drawio.py`（29 个用例 + 库内存量文件回归）。

### Step 4: 导出 PNG 预览并检查

`.drawio` 是 XML 源文件，必须渲染出图才算真正验证过。

```bash
# macOS（本机已验证可用）
"/Applications/draw.io.app/Contents/MacOS/draw.io" \
  --export --format png --scale 2 \
  --output <file>.png <file>.drawio
```

- PNG 与 `.drawio` **同目录同名**
- 多页文件加 `--page-index N`（从 1 起）逐页导出检查

**视觉检查清单**（对着 PNG 看）：

- [ ] 表格最右列完整可见（未被裁一半）
- [ ] 元素无重叠，下方元素 y 已随新增行下移
- [ ] 连线不穿过节点或文字
- [ ] 小字号（8-9px）在缩放下仍可读
- [ ] 图例在右上角，3 秒能分清 Part 结构

发现问题 → 修复 → 重跑 Step 3 校验 → **重新导出覆盖 PNG** → 再看。

**含可点击链接的图**：PNG 不含交互，需在 draw.io 编辑器/查看器中 ⌘+点击抽查链接（见 `references/links.md`）。

**无法导出时**（CLI 缺失且无桌面版）：**不得声称"已完成视觉验证"**——明确告知用户本图仅通过 XML 校验、视觉未验证，并给出手动路径：https://app.diagrams.net 打开 → File → Export as → PNG。

### Step 5: 交付

- `.drawio` + `.png` 同目录成对交付
- 报告校验结果（0 error / warning 处置）与预览检查结论

---

## 整体布局

### 标准页面结构

```
┌─────────────────────────────────────────────────┐
│  标题 (text, fontSize=20, fontStyle=1)           │ y=10
│  副标题 (text, fontSize=10, fontColor=#666)       │ y=38
│                                   ┌── 图例 ──┐  │ y=60
│  一、第一部分 (深色标题条)           │ 颜色说明 │  │ y=100
│  ┌─────────────────────────────┐  └─────────┘  │
│  │ 决策树 / 表格 / 流程图       │               │
│  └─────────────────────────────┘               │
│  二、第二部分 (不同颜色标题条)                     │
│  ┌──────┐  ┌──────┐  ┌──────┐                  │
│  │Step 1│→│Step 2│→│Step 3│  (并排布局)        │
│  └──────┘  └──────┘  └──────┘                  │
│  三、第三部分                                    │
│  ┌─────────────────────────────┐               │
│  │ HTML 表格                    │               │
│  └─────────────────────────────┘               │
└─────────────────────────────────────────────────┘
```

### 间距规范

| 元素 | 间距 |
|------|------|
| 标题与第一个 Part | 50-60px |
| Part 标题条与内容 | 10-15px |
| 内容与下一个 Part 标题 | 20-30px |
| 并排元素之间 | 30px |
| 标准页面宽度 | 900-1000px（内容区） |

### 章节标题配色

每个 Part 用不同深色底+白字，一眼分清层次。具体色值见 `references/color-cards.md` →「章节标题条」。

---

## 元素选择（⛔ 禁忌清单）

### ⛔ 绝对不要做的事

| # | 禁忌 | 为什么 | 正确做法 |
|---|------|--------|---------|
| 1 | **在 drawio 里写 markdown 表格** | drawio 不渲染 markdown，显示为原始文本 | 用 HTML `<table>`（校验器报 error） |
| 2 | **用 `shape=table` 样式包裹 HTML 表格** | 双重表格引擎冲突，内容被裁切/大量空白 | 用 `rounded=0;whiteSpace=wrap;html=1;overflow=fill;verticalAlign=top;`（校验器报 error） |
| 3 | **用框的背景色同时表示归属和优先级** | 颜色语义冲突，读者无法区分 | 框色=归属，优先级用 emoji（🔴P0 🟡P1 ⚪P2） |
| 4 | **subgraph 里放超过 5 个节点** | 渲染挤成一团 | 改用表格 |
| 5 | **图例放在图的中间或底部** | 读者找不到 | 图例放右上角，用虚线框 |

### ✅ 推荐元素

| 场景 | 元素 | style 关键属性 |
|------|------|---------------|
| 章节标题 | 矩形（圆角+深色底+白字） | `fillColor=#1565C0;fontColor=#fff;rounded=1;fontSize=14;fontStyle=1;` |
| 决策节点 | 菱形（黄色） | `rhombus;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;` |
| 结果节点 | 矩形（绿/红/蓝底） | `rounded=1;fillColor=#d5e8d4;strokeColor=#2E7D32;` |
| 数据表格 | mxCell + HTML `<table>` | `rounded=0;whiteSpace=wrap;html=1;overflow=fill;verticalAlign=top;` |
| 起点/终点 | 椭圆 | `ellipse;fillColor=#f8cecc;strokeColor=#b85450;` |
| 可点击链接 | UserObject | `<UserObject label="文字" link="URL">` |
| 说明文字 | text 元素 | `text;html=1;fontSize=10;fontColor=#666;` |

---

## 最小可运行骨架（复制即用）

新建 drawio 文件时，复制以下骨架开始：

```xml
<mxfile host="app.diagrams.net" modified="2026-01-01T00:00:00.000Z" agent="Cursor" version="24.7.6">
  <diagram id="main" name="图表名">
    <mxGraphModel dx="1600" dy="1400" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="1600" pageHeight="1400" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- 标题 -->
        <mxCell id="title" value="标题" style="text;html=1;fontSize=20;fontStyle=1;align=center;" vertex="1" parent="1">
          <mxGeometry x="50" y="10" width="900" height="30" as="geometry" />
        </mxCell>
        <mxCell id="subtitle" value="副标题 | 日期" style="text;html=1;fontSize=10;align=center;fontColor=#666;" vertex="1" parent="1">
          <mxGeometry x="50" y="38" width="900" height="16" as="geometry" />
        </mxCell>

        <!-- 正文从 y=100 开始 -->

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

关键参数：
- `page="0"` — 不限制页面边界（推荐，内容可以自由扩展）
- `pageHeight` — 设为 `最后元素 y + height + 50`
- 多 tab：在 `<mxfile>` 下加多个 `<diagram>` 节点

---

## 视觉自检清单（校验通过后、交付前）

机器查过的不再列（id 引用、禁忌、html=1、列宽 → 校验器；裁剪/重叠 → PNG 预览）。这里只留预览图上看不出来的：

| # | 检查项 | 方法 |
|---|--------|------|
| 1 | 颜色只表达一个维度？ | 对照 `references/color-cards.md` 语义表，确认只有一个语义系统 |
| 2 | 可点击链接写法正确且抽查过？ | 独立元素用 UserObject、表格内用 `<a href>`；⌘+点击至少各验证一个 |
| 3 | 内容顺序符合阅读动线？ | 从上到下、先结论后细节；灰度下也能靠文字/emoji 区分信息 |
| 4 | 交付物成对且最新？ | `.drawio` 与 `.png` 同目录同名，PNG 是最终版导出 |

---

## 与其他 skill 的关系

| Skill | 关系 |
|-------|------|
| `monitoring-drawio-conventions` | 监控图的**专属颜色规范**（归属色、通知标签、服务区分色）。画监控相关 drawio 时，先按本 skill 选图类型和布局，再按那个 skill 上色。 |
| `executive-reporting` | **文档写作**方法论（结果前置、受众感知）。本 skill 只管 drawio 图的画法，文档正文按那个 skill 写。 |
