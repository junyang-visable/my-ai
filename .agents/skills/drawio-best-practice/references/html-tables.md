# HTML 表格模板（核心技能）

> **何时读**：图里要放结构化数据/表格时，生成前**必读**。
> drawio 中展示结构化数据，**必须用 HTML `<table>`**。以下模板与规则均经真实渲染验证。
> 拆分自 SKILL.md，规则本身不变。

## 最小可用表格

```xml
<mxCell id="my-table" value="&lt;table border='1' cellpadding='4' cellspacing='0' style='border-collapse:collapse;font-size:9px;width:100%;'&gt;&lt;tr style='background:#1565C0;color:#fff;font-weight:bold;'&gt;&lt;td&gt;列1&lt;/td&gt;&lt;td&gt;列2&lt;/td&gt;&lt;td&gt;列3&lt;/td&gt;&lt;/tr&gt;&lt;tr&gt;&lt;td&gt;数据&lt;/td&gt;&lt;td&gt;数据&lt;/td&gt;&lt;td&gt;数据&lt;/td&gt;&lt;/tr&gt;&lt;tr style='background:#f5f5f5;'&gt;&lt;td&gt;交替行&lt;/td&gt;&lt;td&gt;灰底&lt;/td&gt;&lt;td&gt;更易读&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;" style="rounded=0;whiteSpace=wrap;html=1;overflow=fill;verticalAlign=top;" vertex="1" parent="1">
  <mxGeometry x="50" y="100" width="900" height="80" as="geometry" />
</mxCell>
```

## 关键规则

1. **style 不能有 `shape=table`** — 这是最常见的坑，加了就会裁切（校验器会报 error）
2. **`overflow=fill`** — 让内容撑满单元格
3. **`width:100%`** — 表格宽度占满 mxCell，但**列宽总和必须小于 cell 宽**（见规则 8，否则最右列被裁剪）
4. **交替行用 `background:#f5f5f5`** — 提升可读性
5. **表头深色底白字** — 一眼区分表头和数据
6. **height 用浏览器实测，不预估** — 「每行约 20-25px」的预估系统性偏差大（实测 9px 字号 + cellpadding=4 时单行约 19-21px，空隙/换行差异累积后偏差更大）；把表格 HTML 注入复刻 drawio 渲染参数的测量页（font-family:Helvetica,Arial + **无单位** line-height:1.2，写 1.2em 会按父级 16px 解析致高度虚高约 30%），读 `table.offsetHeight` 回写 height = 实测值 + 2px
7. **HTML 实体转义** — value 中 `<` 写成 `&lt;`、`>` 写成 `&gt;`、`&` 写成 `&amp;`（drawio XML 要求）
8. **列宽总和 + 开销 ≤ cell 宽（防最右列被裁）** — td 是 content-box，表格实际渲染宽 = 列宽总和 + cellpadding×2×列数 + 边框（约 9px/列）。列宽总和 == cell 宽时表格右溢出 37-55px，**最右列（如「查看链接」列）被 drawio 内部 overflow:hidden 中间层裁掉 40-60%**。正确做法：cell 宽 ≥ 列宽总和 + 9px×列数 + 4px（如 6 列总宽 1300 → cell 至少 1360）；列宽总和小于 cell 时 `width:100%` + `table-layout:fixed` 会自动分配余量，不会破坏布局
9. **列宽用 `<td style='width:Npx;'>`，表格加 `table-layout:fixed`** — `<td width='N'>` 属性写法会被 drawio 引擎忽略，长文本列自动扩宽挤掉其他列；`table-layout:fixed` 固定列宽不被内容撑开
10. **长文本列加 `word-break:break-all`** — 过滤表达式、URL 等长串防止把表格撑出 cell

规则 8 与 10 有校验器兜底：列宽疑似溢出会报 warning，但仍需 PNG 预览确认。

## 颜色行表示状态

```xml
<!-- 正常行 -->
<tr style='background:#d5e8d4;'>  <!-- 绿色 = 通过/安全 -->
<!-- 警告行 -->
<tr style='background:#fff2cc;'>  <!-- 黄色 = 注意 -->
<!-- 危险行 -->
<tr style='background:#f8cecc;'>  <!-- 红色 = 危险/阻断 -->
```

---

## 两种表格方式的选择指南

| 场景 | 用 mxCell 拼表格 | 用 HTML `<table>` |
|------|-----------------|-------------------|
| 每个单元格需要独立颜色 | ✅ 最佳 | 也行（用 `<td style>`) |
| 需要合并单元格/嵌套表头 | ✅ 最佳 | HTML colspan 也行 |
| 行数 > 10 行 | ❌ 太多节点 | ✅ 最佳 |
| 简单对比表 | ❌ 过度 | ✅ 最佳 |
| 需要在图中和其他元素混排 | ✅ 灵活 | ✅ 也行 |

**经验法则**：核心矩阵（行列 < 8×8 且需要独立配色）→ mxCell 拼；大量数据行 → HTML `<table>`。

mxCell 拼表格的对齐秘诀：每列宽度之和 = 总宽度，相邻 cell 的 `x + width = 下一个 cell 的 x`（完整示例见 `examples.md` 示例 B）。
