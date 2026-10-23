# 常见错误速查

> **何时读**：校验报错、或 PNG 预览与预期不符时对照排查。
> 拆分自 SKILL.md，内容本身不变。

| 现象 | 原因 | 修复 |
|------|------|------|
| HTML 表格大量空白/被裁切 | mxCell style 里有 `shape=table` | 删掉 `shape=table`，用 `overflow=fill` |
| 表格内容不显示 | 缺少 `html=1` | 加 `html=1;whiteSpace=wrap;` |
| 颜色混乱看不懂 | 一个颜色同时表达归属和优先级 | 颜色只做一件事，优先级用 emoji |
| 混合归属框里颜色矛盾 | 绿框里有蓝色团队的内容 | 框用 `#f5f5f5` 灰白，靠 🟢/🔵 前缀 |
| 独立元素链接不可点击 | 链接以纯文本写在 mxCell value 里 | 用 `<UserObject link="URL">` 包裹（表格内则改用 `<a href>`，见 `links.md`） |
| 元素重叠 | 新增行后没更新下方元素的 y 坐标 | 每次加行，下方所有元素 y 都要 + 行高 |
| 图太大打不开 | 内容全挤一页 | 拆成多个 diagram（drawio 支持多 tab） |
| HTML 表格中 `>` `<` 显示异常 | 未做 XML 实体转义 | `>` → `&amp;gt;`、`<` → `&amp;lt;` |
| mxCell 拼的表格有缝隙 | 相邻 cell 的 x+width ≠ 下一个 x | 严格计算：`x₂ = x₁ + width₁` |
| 表格最右列看不见/被裁一半 | 列宽总和 + padding 开销 ≥ cell 宽，被内部 overflow:hidden 层裁剪 | cell 宽 ≥ 列宽总和 + 9px×列数 + 4px |
| 设了列宽但不生效 | 用了 `<td width='N'>` 属性写法（引擎忽略） | `<td style='width:Npx;'>` + 表格 `table-layout:fixed` |
| 长文本把表格撑出 cell | 长表达式/URL 撑宽列 | 该列 `<td style='word-break:break-all;'>` |
| 本地验证通过但用户看不到列 | 量错了对比容器（foreignObject 是全画布尺寸，永远"装得下"） | 量表格右缘 vs cell 尺寸中间层：`fo.firstElementChild.firstElementChild` |
| 表格底部大片空白/内容被裁 | height 按每行 20-25px 预估，系统性偏差 | 浏览器实测 offsetHeight 回写（见 `html-tables.md` 关键规则 6） |
| id 重复导致连线指错对象 | 复制节点后忘记改 id | 校验器会报 error；引用只认 id，复制块必须全部改新 id |
