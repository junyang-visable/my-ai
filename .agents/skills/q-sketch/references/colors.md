# 色彩规范

三种配色主题的完整色表与色调浓度档位。生成 prompt 时按用户指定的主题选用对应色值。

## 主题一：暖橙（默认）

适合团队协作、文化建设、通用技术分享类文章。

| 角色 | 色值 | 用途 |
|------|------|------|
| 背景色 | Cream #FFFAF0 | 主背景，纸张质感 |
| 辅助背景 | Soft Peach #FED7AA | 强调区域、卡片底色 |
| 主色 | Warm Orange #ED8936 | 主要强调色、标题装饰 |
| 辅助色 | Golden Yellow #F6AD55 | 温暖感、高光、次要强调 |
| 深色 | Terracotta #C05621 | 深度、重点文字、边框 |
| 锚定色 | Deep Brown #744210 | 接地元素、正文文字 |
| 点缀色 | Soft Red #E53E3E | 情感表达、错误/警告标记 |
| 文字色 | Warm Charcoal #4A4A4A | 标注文字 |
| 失败/灰调 | Muted Gray #9CA3AF / #CBD5E0 | 表示失败、旧方案、被动状态 |

## 主题二：浅绿

适合教程、最佳实践、DevOps 流程、新手指南类文章。明亮清新，通透感强。

| 角色 | 色值 | 用途 |
|------|------|------|
| 背景色 | Warm Cream #FFFDF5 | 主背景，柔和纸张质感 |
| 辅助背景 | Soft Mint #A7F3D0 | 强调区域、卡片底色 |
| 主色 | Sage Green #86EFAC | 主要强调色、标题装饰 |
| 辅助色 | Warm Lime #BEF264 | 活力感、高光、次要强调 |
| 深色 | Gentle Olive #84CC16 | 深度、重点文字、边框 |
| 锚定色 | Forest Green #166534 (20%) | 接地元素、正文文字 |
| 点缀色 | Soft Teal #5EEAD4 | 情感表达、高亮标记 |
| 文字色 | Dark Sage #374151 | 标注文字 |
| 失败/灰调 | Muted Gray #9CA3AF / #CBD5E0 | 表示失败、旧方案、被动状态 |

## 主题三：暗夜暖金

适合夜间模式、架构深度解析、深夜复盘、安全/监控类文章。深底暖光，像深夜台灯下的工作台。

| 角色 | 色值 | 用途 |
|------|------|------|
| 背景色 | Deep Charcoal #1C1917 | 主背景，深棕炭色 |
| 辅助背景 | Warm Dark #292524 | 强调区域、卡片底色 |
| 主色 | Amber Gold #F59E0B | 主要强调色、标题装饰 |
| 辅助色 | Warm Honey #FBBF24 | 温暖感、高光、次要强调 |
| 深色 | Burnt Sienna #92400E | 深度、重点边框 |
| 锚定色 | Light Cream #FEF3C7 | 正文文字、图标 |
| 点缀色 | Soft Coral #FB923C | 情感表达、高亮标记 |
| 文字色 | Pale Warm #FDE68A | 标注文字 |
| 失败/灰调 | Dark Warm Gray #57534E / #78716C | 表示失败、旧方案、被动状态 |

## 色调浓度档位

生成 prompt 时根据用户需求选择浓度档位，默认使用「标准」档：

| 档位 | Prompt 关键词 | 适用场景 |
|------|--------------|----------|
| 标准 | warm watercolor washes, soft watercolor coloring | 大多数配图，色彩饱满温暖 |
| 偏浅 | VERY LIGHT watercolor washes, diluted colors at 50% opacity | 系列配图、需要文字叠加的底图 |
| 极浅 | EXTREMELY LIGHT PASTEL washes, colors at 30% opacity, airy dreamy | 封面装饰、背景插图、追求透气感 |

切换档位时只需替换通用前缀中 STYLE 段落里对色彩浓度的描述，其余不变。
