# 完整标注示例与标杆索引

> **何时读**：不确定布局怎么组织、或想参考同类图的成熟结构时。
> 拆分自 SKILL.md，内容本身不变。

## 示例 A：应急预案（决策树 + SOP + 速查表 + 升级路径）

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

## 示例 B：故障等级矩阵（原生表格 + HTML 表格 + 图例）

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

## MD 转 drawio 标准演示样本

**标准输入示例**：`nexus_incident_severity_definition.md`（v2.1）
**标准输出示例**：`nexus_incident_severity_matrix.drawio`（即示例 B）

## 标杆案例索引

> 注：nexus 系列原文件存于原作者机器（`/Users/lw/code/lw/lw_cron/`），本仓库不可读——下表保留作图型与亮点参考；本仓库可读的标杆见最后一行。

| 文件 | 图类型 | 亮点 | 路径 |
|------|--------|------|------|
| 应急预案 | 决策树 + SOP + 速查表 | 老板点名表扬"画的很不错" | `nexus_incident_response_plan.drawio` |
| 故障矩阵 | mxCell 原生拼 + HTML 表格 | 核心区 mxCell 独立配色，观测区 HTML | `nexus_incident_severity_matrix.drawio` |
| 方案选型 | 4 方案卡片 + 对比表 + 决策树 | 一图看完所有选择 | `nexus_biz_metric_4_approaches.drawio` |
| 监控全景 | 分层全景 + 归属颜色 + 通知标签 | 全域监控一页看完 | `nexus_connection_monitoring_overview.drawio` |
| 需求跟踪 | 可点击 Jira 链接 + UserObject | 点击直达 Jira | `nexus_dragon_release_tracker.drawio` |
| 报表导航 | 分区卡片 + 链接 | Redash+DD+Tableau 全导航 | `nexus_redash_qdr_reports.drawio` |
| 告警能力清单 | HTML 表格 + 链接列 + 列宽 slack | 5 表 110 行、80 个 `<a href>` 可点击链接、列宽总和 + 开销 < cell 宽防裁剪 | 本仓库 `knowledge-base/V-Frontend-Monitor-告警能力清单.drawio` |
