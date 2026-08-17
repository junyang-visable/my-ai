---
name: drawio-best-practice
description: 画易读易懂的 drawio 图的方法论。支持 MD 文档自动转 drawio。Use when user mentions drawio、画图、架构图、流程图、矩阵图、对比图、决策树、应急预案图、监控全景图、draw.io、画个图出来、转drawio、生成drawio、md转图.
---

# Drawio 最佳实践 — 最小成本画出阅读成本最低的图

## MD 文档 → drawio 自动生成工作流

当用户提供 MD 文档并要求生成 drawio 时，按以下 4 步执行：

### Step 1: 分析文档结构

读取 MD 文档，识别信息类型：

| MD 中的结构 | 映射为 drawio 图类型 |
|------------|---------------------|
| `# 标题` + `## 子标题` | drawio 的 Part 章节（深色标题条） |
| markdown 表格 `\|...\|` | HTML `<table>`（直接转换，加颜色行） |
| 有序列表 `1. 2. 3.` | 并排 SOP 步骤框（矩形 + 箭头） |
| 条件判断 "如果...则..." | 决策树（菱形 + 矩形） |
| 分类/分组 `### 类别A` | 分区卡片或表格分组行 |
| 优先级标记 P0/P1/P2 | 颜色编码（红/黄/绿） |
| 链接 `[text](url)` | UserObject 可点击链接 |
| 指标/数据 | 数值直接填入表格单元格 |

### Step 2: 选择布局

根据 Step 1 识别的信息类型组合，选择布局：

```
纯表格内容 → 单表格布局（标题 + 一个大 HTML table）
表格 + 流程 → 混合布局（上半部分流程图，下半部分表格）
多步骤操作 → SOP 布局（并排步骤框 + 箭头）
条件判断 + 结果 → 决策树布局（菱形 → 矩形）
分层分类 → 分区布局（多个 Part，每个 Part 有独立标题色）
```

### Step 3: 生成 drawio XML

按本 skill 的规范（色卡、禁忌、模板）生成 XML，写入 `.drawio` 文件。

### Step 4: 自检

对照本 skill 的「自检清单」逐项检查，确保无遗漏。

**标准输入示例**：`nexus_incident_severity_definition.md`（v2.1）
**标准输出示例**：`nexus_incident_severity_matrix.drawio`

演示时把该 MD 丢给 agent，说「按 drawio-best-practice 画图」即可。

---

## 核心原则

**一张好图 = 3 秒抓住结构 + 30 秒看懂细节。**

做到这一点只需要三件事：
1. **选对图类型**（决策树 vs 表格 vs 流程）
2. **用对 drawio 元素**（原生形状 + HTML 表格，不用 markdown）
3. **颜色只做一件事**（区分归属 OR 区分优先级，不能同时两种语义）

---

## 第一步：选图类型

拿到需求后第一个问题：**这个信息适合用什么结构展示？**

| 信息类型 | 用什么 | 不用什么 | 参考文件 |
|---------|--------|---------|---------|
| **是/否判断链** | 决策树（菱形+矩形） | 表格 | `nexus_incident_response_plan.drawio` Part 1 |
| **多步骤操作** | 并排矩形 + 箭头 | 纯文字列表 | `nexus_incident_response_plan.drawio` Part 2 |
| **多维度对比** | HTML `<table>` | markdown 表格 / shape=table | `nexus_biz_metric_4_approaches.drawio` 对比表 |
| **指标矩阵** | HTML `<table>` + 颜色行 | 一堆小方块 | `nexus_incident_severity_matrix.drawio` |
| **全景/拓扑** | 分层布局 + 归属颜色 | 所有东西挤一层 | `nexus_connection_monitoring_overview.drawio` |
| **升级路径** | 横向节点 + 箭头 | 纯文字 | `nexus_incident_response_plan.drawio` Part 5 |
| **场景速查** | HTML `<table>` 带颜色行 | 每个场景一个大框 | `nexus_incident_response_plan.drawio` Part 3 |

**关键决策：表格 vs 图形？**
- 信息是"分类列表" → **表格**（阅读成本最低）
- 信息有"流向/因果/顺序" → **图形**（箭头表达关系）
- 两者都有 → **混合**（上半部分决策树，下半部分表格）

---

## 标准色卡（所有 drawio 通用）

### 节点填充色 + 边框色（浅底深框原则）

| 语义 | fillColor（浅底） | strokeColor（深框） | 用途 |
|------|-------------------|-------------------|------|
| 安全/通过/完成 | `#d5e8d4` 浅绿 | `#82b366` / `#2E7D32` | 正常状态、通过、绿灯 |
| 警告/注意/判断 | `#fff2cc` 浅黄 | `#d6b656` | 条件节点、需关注 |
| 危险/错误/阻断 | `#f8cecc` 浅红 | `#b85450` | 失败、P0、阻断 |
| 信息/步骤/操作 | `#dae8fc` 浅蓝 | `#6c8ebf` | 流程步骤、操作框 |
| ALI 相关 | `#fce5cd` 浅橙 | `#e69138` | Alibaba 适配层 |
| 跨域/通用 | `#e1d5e7` 浅紫 | `#9673a6` | 对比表标题、决策树 |
| 中性/外部/禁用 | `#e6e6e6` 浅灰 | `#999999` | 已废弃、外部依赖 |
| 混合归属 | `#f5f5f5` 灰白 | `#cccccc` | 多团队混合内容 |

### 章节标题条（深色底 + 白字 `fontColor=#fff`）

| Part | fillColor | 色名 |
|------|-----------|------|
| 一 | `#b85450` | 深红 |
| 二 | `#1565C0` | 深蓝 |
| 三 | `#E65100` | 深橙 |
| 四 | `#4527A0` | 深紫 |
| 五 | `#37474F` | 深灰 |

### HTML 表格行颜色

| 用途 | background 值 |
|------|---------------|
| 表头 | `#1565C0` (蓝) / `#e1d5e7` (紫) / `#ffe6cc` (橙) — 配合章节主题色 |
| 普通行 | 无（白底） |
| 交替行 | `#f5f5f5` |
| 安全行 | `#d5e8d4` |
| 警告行 | `#fff2cc` |
| 危险行 | `#f8cecc` |

### 连线 / 箭头

| 用途 | strokeColor | strokeWidth |
|------|-------------|-------------|
| 普通连线 | 默认黑 | 2 |
| 步骤流转 | `#1565C0` 蓝 | 3 |
| "是" 分支 | `#2E7D32` 绿 | 2 |
| "否" 分支 | `#b85450` 红 | 2 |

### 文字颜色

| 用途 | fontColor |
|------|-----------|
| 正文 | 默认黑 |
| 副标题/说明 | `#666` / `#999` |
| 深色底上的字 | `#fff` |
| "是" 标签 | `#2E7D32` |
| "否" 标签 | `#b85450` |

---

## 第二步：drawio 元素选择（⛔ 禁忌清单）

### ⛔ 绝对不要做的事

| # | 禁忌 | 为什么 | 正确做法 |
|---|------|--------|---------|
| 1 | **在 drawio 里写 markdown 表格** | drawio 不渲染 markdown，显示为原始文本 | 用 HTML `<table>` |
| 2 | **用 `shape=table` 样式包裹 HTML 表格** | 双重表格引擎冲突，内容被裁切/大量空白 | 用 `rounded=0;whiteSpace=wrap;html=1;overflow=fill;verticalAlign=top;` |
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

## 第三步：HTML 表格模板（核心技能）

drawio 中展示结构化数据，**必须用 HTML `<table>`**。以下是经过验证的模板：

### 最小可用表格

```xml
<mxCell id="my-table" value="&lt;table border='1' cellpadding='4' cellspacing='0' style='border-collapse:collapse;font-size:9px;width:100%;'&gt;&lt;tr style='background:#1565C0;color:#fff;font-weight:bold;'&gt;&lt;td&gt;列1&lt;/td&gt;&lt;td&gt;列2&lt;/td&gt;&lt;td&gt;列3&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td&gt;数据&lt;/td&gt;&lt;td&gt;数据&lt;/td&gt;&lt;td&gt;数据&lt;/td&gt;&lt;/tr&gt;&lt;tr style='background:#f5f5f5;'&gt;&lt;td&gt;交替行&lt;/td&gt;&lt;td&gt;灰底&lt;/td&gt;&lt;td&gt;更易读&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;" style="rounded=0;whiteSpace=wrap;html=1;overflow=fill;verticalAlign=top;" vertex="1" parent="1">
  <mxGeometry x="50" y="100" width="900" height="80" as="geometry" />
</mxCell>
```

### 关键规则

1. **style 不能有 `shape=table`** — 这是最常见的坑，加了就会裁切
2. **`overflow=fill`** — 让内容撑满单元格
3. **`width:100%`** — 表格宽度占满 mxCell
4. **交替行用 `background:#f5f5f5`** — 提升可读性
5. **表头深色底白字** — 一眼区分表头和数据
6. **height 要手动预估** — 每行约 20-25px，算好后设到 `<mxGeometry>`
7. **HTML 实体转义** — value 中 `<` 写成 `&lt;`、`>` 写成 `&gt;`、`&` 写成 `&amp;`（drawio XML 要求）

### 颜色行表示状态

```xml
<!-- 正常行 -->
<tr style='background:#d5e8d4;'>  <!-- 绿色 = 通过/安全 -->
<!-- 警告行 -->
<tr style='background:#fff2cc;'>  <!-- 黄色 = 注意 -->
<!-- 危险行 -->
<tr style='background:#f8cecc;'>  <!-- 红色 = 危险/阻断 -->
```

---

## 第四步：整体布局

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

每个 Part 用不同深色底+白字，一眼分清层次。具体色值见上方「标准色卡 → 章节标题条」。

---

## 第五步：颜色语义（一图只做一件事）

### 规则：一张图中颜色只表达一个维度

| 场景 | 颜色表达 | 优先级怎么标 |
|------|---------|-------------|
| 监控全景图 | 归属（绿=Dragon, 蓝=VCN, 红=待建） | emoji 前缀 🔴🟡⚪ |
| 故障矩阵 | 故障等级（红=P0, 黄=P1, 绿=P2） | 无需额外标 |
| 埋点方案 | 服务（橙=alivis, 蓝=requests） | emoji 前缀 🔴🟡⚪ |
| 方案对比 | 推荐度（绿=推荐, 蓝=备选, 灰=不推荐） | 无需额外标 |

### 混合归属单元格

一个框里有多个团队的内容时，**框用灰白 `#f5f5f5`**，靠文字前缀区分：

```
❌ 绿色框里放 🔵 VCN 的内容（矛盾）
✅ 灰白框，每行用 🟢/🔵 前缀标归属
```

---

## 第六步：可点击链接

drawio 中要做可点击的链接（如跳转 Jira），必须用 `UserObject`：

```xml
<UserObject label="DRG-1234 需求描述" link="https://visable.atlassian.net/browse/DRG-1234" id="xxx">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="200" height="30" as="geometry" />
  </mxCell>
</UserObject>
```

普通 `mxCell` 的 `value` 里写链接是**不可点击**的。

---

## 完整标注示例

### 示例 A：应急预案（决策树 + SOP + 速查表 + 升级路径）

**文件**：`nexus_incident_response_plan.drawio`（老板点名表扬）

**结构拆解** — 5 个 Part 用了 4 种图类型：

```
Part 一 (红标题) → 决策树：椭圆起点 → 3 级菱形判断 → 矩形结果 + 速查表
Part 二 (蓝标题) → 并排 SOP：3 列矩形 Step1→Step2→Step3 粗箭头连接
Part 三 (橙标题) → 场景速查：HTML <table> 带颜色行 (红=P0, 黄=P1)
Part 四 (紫标题) → 演练 Checklist：HTML <table> 交替行
Part 五 (深灰标题) → 升级路径：5 个横排节点 + 箭头标等级
```

**关键代码片段 — 决策树部分**：

```xml
<!-- 起点: 椭圆 (红底) -->
<mxCell id="d-start" value="故障发生" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=11;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="420" y="100" width="120" height="40" as="geometry" />
</mxCell>

<!-- 判断节点: 菱形 (黄底), 放在起点正下方 -->
<mxCell id="q1" value="最近 24h 内&lt;br&gt;有部署吗？" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=10;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="405" y="160" width="150" height="70" as="geometry" />
</mxCell>

<!-- "否" → 左边绿色结果框 -->
<mxCell id="q1-no-box" value="非代码问题&lt;br&gt;&lt;b&gt;不回滚，直接排查&lt;/b&gt;&lt;br&gt;&lt;font style='font-size:8px'&gt;→ 查外部依赖&lt;br&gt;→ 查基础设施&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e8f5e9;strokeColor=#82b366;fontSize=9;" vertex="1" parent="1">
  <mxGeometry x="100" y="168" width="220" height="75" as="geometry" />
</mxCell>

<!-- 连线: 否=红字左走, 是=绿字下走 -->
<mxCell value="否" style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;fontStyle=1;fontSize=10;fontColor=#b85450;" edge="1" parent="1" source="q1" target="q1-no-box" />
<mxCell value="是" style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;fontStyle=1;fontSize=10;fontColor=#2E7D32;" edge="1" parent="1" source="q1" target="q2" />
```

**关键代码片段 — 并排 SOP 部分**：

```xml
<!-- 步骤框: 内部用 <div>+<hr>+<b> 排版, 三列等宽 280px, 间距 30px -->
<mxCell id="step1" value="&lt;div style='text-align:center;font-size:12px;font-weight:bold;margin-bottom:4px;'&gt;Step 1: 代码回滚&lt;/div&gt;&lt;hr style='margin:2px 0'&gt;&lt;div style='font-size:9px;text-align:left;'&gt;&lt;b&gt;方式 A: GitHub Revert (推荐)&lt;/b&gt;&lt;br&gt;① GitHub → 找到出问题的 Merge PR&lt;br&gt;② 点 Revert → 创建 Revert PR&lt;/div&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;overflow=fill;verticalAlign=top;spacingLeft=6;spacingTop=4;" vertex="1" parent="1">
  <mxGeometry x="50" y="650" width="280" height="250" as="geometry" />
</mxCell>

<!-- 粗箭头连接步骤 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;strokeColor=#1565C0;strokeWidth=3;" edge="1" parent="1" source="step1" target="step2" />
```

**关键代码片段 — 场景速查 HTML 表格**：

```xml
<!-- 颜色行区分 P0(红) P1(黄) P2(白), 表头用 Part 同色 -->
<mxCell id="scenario-table" value="&lt;table border='1' cellpadding='4' cellspacing='0' style='border-collapse:collapse;font-size:9px;width:100%;'&gt;&lt;tr style='background:#E65100;color:#fff;font-weight:bold;'&gt;&lt;td&gt;#&lt;/td&gt;&lt;td&gt;场景&lt;/td&gt;&lt;td&gt;级别&lt;/td&gt;&lt;td&gt;触发信号&lt;/td&gt;&lt;td&gt;可回滚?&lt;/td&gt;&lt;td&gt;排查→恢复&lt;/td&gt;&lt;/tr&gt;&lt;tr style='background:#f8cecc;'&gt;&lt;td&gt;1&lt;/td&gt;&lt;td&gt;&lt;b&gt;ALI链路中断&lt;/b&gt;&lt;/td&gt;&lt;td&gt;🔴P0&lt;/td&gt;&lt;td&gt;event_record DONE=0&lt;/td&gt;&lt;td&gt;❌&lt;/td&gt;&lt;td&gt;查Lambda→查DTS&lt;/td&gt;&lt;/tr&gt;&lt;tr style='background:#fff2cc;'&gt;&lt;td&gt;2&lt;/td&gt;&lt;td&gt;&lt;b&gt;指标暴跌&lt;/b&gt;&lt;/td&gt;&lt;td&gt;🟡P1&lt;/td&gt;&lt;td&gt;跌&amp;gt;30%&lt;/td&gt;&lt;td&gt;看情况&lt;/td&gt;&lt;td&gt;分维度定位&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;" style="rounded=0;whiteSpace=wrap;html=1;overflow=fill;verticalAlign=top;" vertex="1" parent="1">
  <mxGeometry x="50" y="950" width="900" height="220" as="geometry" />
</mxCell>
```

**关键代码片段 — 升级路径**：

```xml
<!-- 5 个横排节点, 每个间距 180px, 颜色由冷到热 -->
<mxCell id="esc-n1" value="VCN 值班" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="80" y="1460" width="100" height="35" as="geometry" />
</mxCell>
<mxCell id="esc-n2" value="Dragon TL" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" ... />
<mxCell id="esc-n3" value="PO" style="...fillColor=#fff2cc;strokeColor=#d6b656;" ... />
<mxCell id="esc-n4" value="EM" style="...fillColor=#f8cecc;strokeColor=#b85450;" ... />

<!-- 箭头标等级, 颜色随等级加深 -->
<mxCell value="P2" style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;" edge="1" source="esc-n1" target="esc-n2" />
<mxCell value="P1" style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;strokeColor=#d6b656;" edge="1" source="esc-n2" target="esc-n3" />
<mxCell value="P0" style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;strokeColor=#b85450;" edge="1" source="esc-n3" target="esc-n4" />
```

---

### 示例 B：故障等级矩阵（原生表格 + HTML 表格 + 图例）

**文件**：`nexus_incident_severity_matrix.drawio`

**结构拆解** — 3 个 Part，表格为主：

```
图例 (虚线框, 右上角) → P0红/P1黄/P2绿 小色块 + 文字说明
Part 一 (蓝标题) → drawio 原生 mxCell 拼出的表格 (行列对齐, 非 HTML)
Part 二 (深灰标题) → HTML <table> (大量行, 用 HTML 更高效)
Part 三 (紫标题) → 4 个并排卡片 (告警路径)
```

**为什么 Part 一用原生 mxCell 而不是 HTML `<table>`？**

因为每个单元格需要**独立的背景色**来表示 P0/P1/P2，且表头需要合并单元格和嵌套子表头。drawio 原生 mxCell 更灵活：

```xml
<!-- 用 mxCell 拼表格: 每个 cell 独立控制颜色和对齐 -->

<!-- 表头行: 深蓝底白字, 3 列合并 -->
<mxCell id="h-m1" value="③ Verified Request" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1565C0;fontColor=#fff;fontSize=10;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="170" y="130" width="260" height="25" as="geometry" />
</mxCell>

<!-- P0/P1/P2 子表头: 3 色小块紧贴排列 -->
<mxCell id="sh1-p0" value="P0" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=8;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="170" y="155" width="87" height="18" as="geometry" />
</mxCell>
<mxCell id="sh1-p1" value="P1" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=8;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="257" y="155" width="86" height="18" as="geometry" />
</mxCell>
<mxCell id="sh1-p2" value="P2" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#e8f5e9;strokeColor=#82b366;fontSize=8;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="343" y="155" width="87" height="18" as="geometry" />
</mxCell>

<!-- 数据行: V=蓝底, A=橙底 标识平台归属 -->
<mxCell id="r1-dim" value="V QDR" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1565C0;fontSize=10;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="50" y="173" width="120" height="30" as="geometry" />
</mxCell>
<mxCell id="r3-dim" value="A QDR" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#E65100;fontSize=10;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="50" y="233" width="120" height="30" as="geometry" />
</mxCell>
```

**对齐秘诀**：每列宽度之和 = 总宽度，相邻 cell 的 `x + width = 下一个 cell 的 x`：

```
列1(dim): x=50,  w=120  → 50+120=170
列2(P0):  x=170, w=87   → 170+87=257
列3(P1):  x=257, w=86   → 257+86=343
列4(P2):  x=343, w=87   → 343+87=430
列5(P0):  x=430, w=87   → ...
```

**Part 二为什么改用 HTML `<table>`？**

因为技术观测指标有 20+ 行，每行结构相同，用 mxCell 要写 100+ 个节点。HTML 表格一个 mxCell 搞定：

```xml
<mxCell id="tech-table" value="&lt;table border='1' cellpadding='3' cellspacing='0' style='border-collapse:collapse;font-size:9px;width:100%;'&gt;&lt;tr style='background:#37474F;color:#fff;font-weight:bold;'&gt;&lt;td&gt;分类&lt;/td&gt;&lt;td&gt;指标&lt;/td&gt;&lt;td&gt;阈值&lt;/td&gt;&lt;td&gt;方案&lt;/td&gt;&lt;td&gt;覆盖&lt;/td&gt;&lt;/tr&gt;&lt;tr style='background:#ECEFF1;'&gt;&lt;td colspan='5' style='font-weight:bold;'&gt;状态机&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td&gt;S1&lt;/td&gt;&lt;td&gt;b2b_request COMPLETED&lt;/td&gt;&lt;td&gt;跌&amp;gt;40%&lt;/td&gt;&lt;td&gt;Counter/Log&lt;/td&gt;&lt;td&gt;❌&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;" style="rounded=0;whiteSpace=wrap;html=1;overflow=fill;verticalAlign=top;" vertex="1" parent="1">
  <mxGeometry x="50" y="565" width="900" height="440" as="geometry" />
</mxCell>
```

**图例部分**：

```xml
<!-- 虚线框容器 -->
<mxCell id="leg-box" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999;dashed=1;" vertex="1" parent="1">
  <mxGeometry x="50" y="60" width="900" height="28" as="geometry" />
</mxCell>
<!-- 图例色块: 小矩形 + 文字说明, 横排 -->
<mxCell id="leg-p0" value="P0 — 15min 响应" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=9;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="60" y="63" width="120" height="22" as="geometry" />
</mxCell>
<mxCell id="leg-p1" value="P1 — 1h 响应" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=9;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="190" y="63" width="110" height="22" as="geometry" />
</mxCell>
```

---

### 两种表格方式的选择指南

| 场景 | 用 mxCell 拼表格 | 用 HTML `<table>` |
|------|-----------------|-------------------|
| 每个单元格需要独立颜色 | ✅ 最佳 | 也行（用 `<td style>`) |
| 需要合并单元格/嵌套表头 | ✅ 最佳 | HTML colspan 也行 |
| 行数 > 10 行 | ❌ 太多节点 | ✅ 最佳 |
| 简单对比表 | ❌ 过度 | ✅ 最佳 |
| 需要在图中和其他元素混排 | ✅ 灵活 | ✅ 也行 |

**经验法则**：核心矩阵（行列 < 8×8 且需要独立配色）→ mxCell 拼；大量数据行 → HTML `<table>`。

---

## 自检清单（每次画完必检）

| # | 检查项 | 方法 |
|---|--------|------|
| 1 | 3 秒能看到整体结构？ | 缩放到全图，能分清几个 Part |
| 2 | 颜色只表达一个维度？ | 数颜色数量，确认只有一个语义系统 |
| 3 | 没有 markdown 表格？ | 搜索 `\|---\|`，不应存在 |
| 4 | 没有 shape=table？ | 搜索 `shape=table`，不应存在 |
| 5 | 图例在右上角？ | 确认存在虚线框图例 |
| 6 | HTML 表格有交替行？ | 确认偶数行有 `background:#f5f5f5` |
| 7 | 所有 Part 标题有颜色条？ | 确认每个章节有深色标题 |
| 8 | y 坐标没有重叠？ | 上一元素 y+height < 下一元素 y |
| 9 | 可点击链接用 UserObject？ | 搜索 `link=`，确认在 `UserObject` 中 |
| 10 | 页面高度够？ | `pageHeight` > 最后元素的 y+height |

---

## 参考文件索引

| 文件 | 图类型 | 亮点 | 路径 |
|------|--------|------|------|
| 应急预案 | 决策树 + SOP + 速查表 | 老板点名表扬"画的很不错" | `nexus_incident_response_plan.drawio` |
| 故障矩阵 | mxCell 原生拼 + HTML 表格 | 核心区 mxCell 独立配色，观测区 HTML | `nexus_incident_severity_matrix.drawio` |
| 方案选型 | 4 方案卡片 + 对比表 + 决策树 | 一图看完所有选择 | `nexus_biz_metric_4_approaches.drawio` |
| 监控全景 | 分层全景 + 归属颜色 + 通知标签 | 全域监控一页看完 | `nexus_connection_monitoring_overview.drawio` |
| 需求跟踪 | 可点击 Jira 链接 + UserObject | 点击直达 Jira | `nexus_dragon_release_tracker.drawio` |
| 报表导航 | 分区卡片 + 链接 | Redash+DD+Tableau 全导航 | `nexus_redash_qdr_reports.drawio` |

所有文件路径: `/Users/lw/code/lw/lw_cron/` 下。

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

## 与其他 skill 的关系

| Skill | 关系 |
|-------|------|
| `monitoring-drawio-conventions` | 监控图的**专属颜色规范**（归属色、通知标签、服务区分色）。画监控相关 drawio 时，先按本 skill 选图类型和布局，再按那个 skill 上色。 |
| `executive-reporting` | **文档写作**方法论（结果前置、受众感知）。本 skill 只管 drawio 图的画法，文档正文按那个 skill 写。 |

---

## 常见错误速查

| 现象 | 原因 | 修复 |
|------|------|------|
| HTML 表格大量空白/被裁切 | mxCell style 里有 `shape=table` | 删掉 `shape=table`，用 `overflow=fill` |
| 表格内容不显示 | 缺少 `html=1` | 加 `html=1;whiteSpace=wrap;` |
| 颜色混乱看不懂 | 一个颜色同时表达归属和优先级 | 颜色只做一件事，优先级用 emoji |
| 混合归属框里颜色矛盾 | 绿框里有蓝色团队的内容 | 框用 `#f5f5f5` 灰白，靠 🟢/🔵 前缀 |
| 链接不可点击 | 链接写在 mxCell value 里 | 用 `<UserObject link="URL">` 包裹 |
| 元素重叠 | 新增行后没更新下方元素的 y 坐标 | 每次加行，下方所有元素 y 都要 + 行高 |
| 图太大打不开 | 内容全挤一页 | 拆成多个 diagram（drawio 支持多 tab） |
| HTML 表格中 `>` `<` 显示异常 | 未做 XML 实体转义 | `>` → `&amp;gt;`、`<` → `&amp;lt;` |
| mxCell 拼的表格有缝隙 | 相邻 cell 的 x+width ≠ 下一个 x | 严格计算：`x₂ = x₁ + width₁` |
