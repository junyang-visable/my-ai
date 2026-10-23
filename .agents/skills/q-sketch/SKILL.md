---
name: q-sketch
description: Q版温暖手绘配图风格。铅笔线稿+暖色水彩+可爱Q版人物，支持暖橙、浅绿、暗夜暖金三种配色主题。适用于技术博客、知识分享/教程、团队协作与工程实践、产品介绍/功能说明、工作流程/方法论可视化等文章配图，也适用于绘本创作、故事插画、科普读物配图等叙事型插画；不适用于严肃商务场合、数据密集的仪表盘/报表、需要精确品牌色的营销物料、科学/学术论文插图。当用户要求"Q版配图""暖色手绘""q-sketch风格""画绘本"，或需要为文章配图/生成插画/创作绘本时使用——即便用户未明确说使用
  q-sketch，只要涉及技术博客、知识分享类文章配图或绘本插画创作，就应主动使用此技能。
allowed-tools: ImageGen
compatibility: 依赖 ImageGen 图像生成工具；配图生成尺寸固定为
  1792x1024（16:9），绘本单页可按需选用竖版/方版。为保证出图效果，推荐使用「极致」及以上档位的模型（如
  qwen3.8-max、cantus、sonus）或 codex。
version: 0.4.0
---

# Q-Sketch

![Q-Sketch](https://img.alicdn.com/imgextra/i2/O1CN01AlzLKJKUNRJ4Zzly_!!6000000006593-2-tps-2256-2026.png)

Q版温暖手绘配图风格 — 铅笔手绘质感 + 暖色水彩渲染 + 可爱Q版人物。适合技术博客、知识分享、团队协作类文章，营造轻松亲切、专业但不冰冷的视觉感受。

## 何时使用

主动触发场景：

- **文章配图**：为技术博客、知识分享、教程、工程实践、产品介绍、流程/方法论类文章配图或生成插画。
- **绘本创作**：绘制绘本、故事插画、科普读物配图等叙事型插画。温暖圆润的 Q 版角色与手绘水彩质感适合故事化、叙事型的连续画面。

**即便用户没有明确说"用 q-sketch"，只要是上述文章配图或绘本插画需求，就使用本技能。**

不适用：严肃商务场合、数据密集的仪表盘/报表、需要精确品牌色的营销物料、科学/学术论文插图。

### 绘本效果示例

![绘本效果示例](https://img.alicdn.com/imgextra/i2/O1CN01WnWZkmNh4gG5sYx2_!!6000000006377-0-tps-2896-2852.jpg)

### 模型推荐

为保证出图效果，推荐使用「极致」及以上档位的模型（如 qwen3.8-max、cantus、sonus）或 codex；低档位模型容易出现线条杂乱、色彩浑浊、角色比例失真等问题。

## 参考资料（按需查阅）

- **色彩规范**：三种主题的完整色表 + 色调浓度档位 → `references/colors.md`
- **人物画法与角色设定**：Q版基本特征、各主题角色服装 Prompt 关键词、线条质感、系列一致性方法 → `references/characters.md`
- **IP 触发词避坑**：避免 ImageGen 报 IPInfringementSuspect 的高危词与安全替代策略 → `references/ip-safety.md`

生成配图前，先读 `references/characters.md` 复制角色 Prompt 关键词（保证系列一致），并按选定主题从 `references/colors.md` 取色值；涉及公主/动漫/宠物等形象时先查 `references/ip-safety.md`。

## 构图规范

- **留白**: 大量留白，画面呼吸感强
- **布局**: 根据内容选择左右对比 / 中心放射 / 2×2网格 / 流程横排
- **分隔**: 手绘线条分隔或自然留白分隔，不使用生硬框线
- **文字**: 中文手写体风格，大而清晰，作为画面的一部分
- **装饰**: 克制使用小星星、波浪线、小心形等，不要过多

## 禁止事项（含原因）

每条禁止都是为了守住"温暖手绘"这一核心风格；违反任一条都会让画面偏离 Q-Sketch 的调性或触发生成失败。

- **彩色渐变或复杂配色** —— 渐变会破坏水彩的柔和晕染质感，复杂配色会稀释暖色系带来的统一温暖氛围。
- **光头或近乎光头的人物** —— Q版角色靠发型区分身份与个性，光头会让角色呆板、难以在系列图中辨识。
- **粗黑边框或生硬分隔线** —— 硬边框是数字化矢量风格，与铅笔手绘的松弛线条相冲突，会显得冰冷。
- **3D 效果、阴影、立体感** —— 本风格是平面手绘水彩，立体渲染会失去纸张质感和亲切的手作温度。
- **写实风格人物** —— 写实比例破坏了 Q版 2.5~3 头身的可爱基调，与整体卡通风格不协调。
- **密集文字堆砌** —— 配图以视觉传达为主，大量文字会挤占留白、丧失呼吸感，应把细节留给正文。
- **冰冷色调（蓝、紫、灰主导）** —— 冷色主导会直接抵消"温暖"这一核心定位，只在灰调点缀用于表示失败/旧方案。
- **数字化的平涂填色** —— 平涂没有水彩的自然晕染边界，会显得死板，必须保留水彩质感。
- **复杂背景或纹理** —— 繁复背景会抢夺主体、压缩留白，与克制、通透的构图原则相悖。

## Prompt 模板

### 通用前缀 - 暖橙主题（默认，所有图片都加）

```
A wide 16:9 hand-drawn warm watercolor illustration. Cute simplified cartoon characters (chibi style - round heads, small dot eyes, small bodies, about 2.5-3 head-to-body ratio).

STYLE: Pencil sketch outlines with warm watercolor washes. Cream background (#FFFAF0) with paper texture feel. Colors: warm orange (#ED8936), golden yellow (#F6AD55), terracotta (#C05621), soft peach (#FED7AA). Characters are cute chibi cartoons with expressive poses. Visible pencil outlines with soft watercolor coloring. Cozy approachable atmosphere. NO harsh edges, NO 3D effects, NO gradients, NO realistic proportions. ALL characters MUST have clearly visible hair (no bald or near-bald characters). Generous white space. Chinese text in handwritten brush style where applicable.
```

### 通用前缀 - 浅绿主题（用户指定浅绿/清新风格时使用）

```
A wide 16:9 hand-drawn watercolor illustration. Cute simplified cartoon characters (chibi style - round heads, small dot eyes, small bodies, about 2.5-3 head-to-body ratio).

STYLE: Pencil sketch outlines with fresh light green watercolor washes. Warm cream background (#FFFDF5) with paper texture feel. Colors: sage green (#86EFAC), warm lime (#BEF264), gentle olive (#84CC16), soft mint (#A7F3D0), soft teal (#5EEAD4). Characters are cute chibi cartoons with expressive poses. Visible pencil outlines with soft watercolor coloring. Bright, cheerful, fresh atmosphere. NO harsh edges, NO 3D effects, NO gradients, NO realistic proportions. ALL characters MUST have clearly visible hair (no bald or near-bald characters). Generous white space. Chinese text in handwritten brush style where applicable.
```

### 通用前缀 - 暗夜暖金主题（用户指定深色/夜间风格时使用）

```
A wide 16:9 hand-drawn watercolor illustration with DARK WARM background. Cute simplified cartoon characters (chibi style - round heads, small dot eyes, small bodies, about 2.5-3 head-to-body ratio).

STYLE: Pencil sketch outlines with warm amber watercolor washes on deep charcoal background (#1C1917). Dark warm brown (#292524) for card areas. Colors: amber gold (#F59E0B), warm honey (#FBBF24), burnt sienna (#92400E), soft coral (#FB923C). Text and labels in light cream (#FEF3C7, #FDE68A). Characters are cute chibi cartoons with expressive poses, glowing warmly against the dark background like a desk lamp scene. Visible pencil outlines with warm watercolor coloring. Cozy late-night atmosphere, warm not cold. NO harsh edges, NO 3D effects, NO gradients, NO realistic proportions. ALL characters MUST have clearly visible hair (no bald or near-bald characters). Chinese text in handwritten brush style where applicable.
```

### 场景类 (Scene)

```
[通用前缀]

COMPOSITION: [描述场景布局]

CHARACTERS:
- [角色1]: [外观] + [动作/表情] + [标注]
- [角色2]: [外观] + [动作/表情] + [标注]

PROPS: [场景中的道具/元素]
MOOD: [整体氛围]
LABELS: [需要显示的中文文字标注]
```

### 对比类 (Comparison)

```
[通用前缀]

LEFT SIDE - "[左侧标题]" ([色调描述]):
- [元素1]
- [元素2]
- Below: handwritten text "[底部文字]"

RIGHT SIDE - "[右侧标题]" ([色调描述]):
- [元素1]
- [元素2]
- Below: handwritten text "[底部文字]"

CENTER DIVIDER: [分隔元素描述]
```

### 框架类 (Framework)

```
[通用前缀]

STRUCTURE: [hierarchical/radial/grid]

CENTER: [中心元素]
NODES radiating outward:
1. "[节点1]" - [小图标描述], [颜色]卡片
2. "[节点2]" - [小图标描述], [颜色]卡片
...

FLOW (bottom): [流程描述]
```

### 信息图类 (Infographic - 2x2 grid)

```
[通用前缀]

Layout: 2x2 grid, each card showing one concept.

CARD 1 - Header "[标题]":
[场景描述]

CARD 2 - Header "[标题]":
[场景描述]

CARD 3 - Header "[标题]":
[场景描述]

CARD 4 - Header "[标题]":
[场景描述]

Each card separated by soft hand-drawn lines. Headers in theme-colored banners (warm orange for 暖橙主题, sage green for 浅绿主题, amber gold for 暗夜暖金主题).
```

## 使用流程

用户说"帮这篇文章配图"时：

1. 分析文章结构，确定需要配图的位置和数量
2. 确定每张图的类型（场景/对比/框架/信息图）
3. 读 `references/characters.md` 复制角色 Prompt 关键词、按主题从 `references/colors.md` 取色值，套用对应模板构建 prompt
4. 生成时使用 `1792x1024` 尺寸（16:9）
5. 系列配图中保持人物角色与风格 Block 一致（方法见 `references/characters.md`）
