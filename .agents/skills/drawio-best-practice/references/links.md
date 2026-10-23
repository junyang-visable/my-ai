# 可点击链接（两种方式，按场景选）

> **何时读**：图里要放可点击链接（Jira、监控、报表）时。
> 拆分自 SKILL.md，规则本身不变。

**方式一：独立元素（节点/按钮/Jira 卡片）→ `UserObject`**

```xml
<UserObject label="DRG-1234 需求描述" link="https://visable.atlassian.net/browse/DRG-1234" id="xxx">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="100" y="100" width="200" height="30" as="geometry" />
  </mxCell>
</UserObject>
```

**方式二：HTML 表格单元格内 → `<a href='URL'>文字</a>`**

```xml
<td style='text-align:center;'><a href='https://app.datadoghq.com/monitors/123'>查看</a></td>
```

- 表格内链接使用时需 **⌘/Ctrl + 点击**（drawio 防误触设计），编辑器与查看器均有效，可在图例中提示用户
- 批量场景（每行一个「查看」链接列）这是唯一可行方案——UserObject 无法嵌入 HTML 表格
- 注意：mxCell value 里的**纯文本 URL**（`value="https://..."`）不可点击，纯文本链接才必须用方式一

**验证提示**：PNG 预览图**不含**链接交互——含链接的图交付前，需在 draw.io 编辑器/查看器里 ⌘+点击抽查至少一个链接（含表格内链接与 UserObject 链接各一），确认跳转正确。
