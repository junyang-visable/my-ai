# 人物画法与角色设定

系列配图中角色外观必须保持一致。生成时从下方「Prompt 关键词」列直接复制对应角色的英文描述，不要每次重新翻译。

## 基本特征（所有人物通用）

- **头身比**: 约 2.5~3 头身（Q版比例）
- **头部**: 圆润大头，占身体比例大
- **五官**: 点状或小圆眼睛，简单弧线嘴巴，极简表情但很传神
- **身体**: 小巧圆润，四肢短粗可爱
- **表情传达**: 通过夸张的肢体动作 + 简单五官变化传达情绪
- **线条**: 铅笔质感的轮廓线，粗细略有变化，不追求完美工整
- **发型**: 所有人物必须有明显的发型，禁止出现光头或近乎光头的人物

## 角色设定表（默认服装，暖橙主题）

| 角色 | 外观特征 | 服装 | Prompt 关键词（直接复制进 prompt） |
|------|----------|------|------|
| 后端开发 | 男生，圆脸，黑框眼镜 | 橙色毛衣/卫衣 | boy, round face, black-framed glasses, short black hair, orange sweater |
| 前端开发 | 男生，蓬松短发 | 灰色/米色帽衫(hoodie) | boy, tousled fluffy short brown hair, grey/beige hoodie |
| 设计师 | 女生，两根麻花辫，齐刘海，戴棒球帽 | 暖色系上衣，手持色卡/画板 | girl, twin braids, straight-cut bangs, baseball cap, warm peach top, holding color swatch card |
| PD/产品 | 男生或女生，干练短发 | 衬衫，手持文档 | person, neat short hair, button-up shirt, holding document |
| 业务方 | 男生，整洁发型 | 衬衫+领带 | boy, neat tidy hair, shirt and tie |
| 测试 | 女生，短发，戴眼镜 | 浅蓝/浅绿色上衣，手持放大镜或测试清单 | girl, short hair, round glasses, light blue top, holding checklist |
| AI 机器人 | 小型可爱机器人，圆脑袋，小天线，简单笑脸 | 白色/浅灰色机身 | small cute robot, round head, small antenna, simple smiley face, white body |

## 浅绿主题服装替换表

使用浅绿主题时，替换上方服装描述，外观特征不变。

| 角色 | 浅绿主题服装 | Prompt 关键词（替换服装部分） |
|------|-------------|------|
| 后端开发 | 鼠尾草绿毛衣 | sage green sweater |
| 前端开发 | 浅薄荷绿帽衫(hoodie) | light mint green hoodie |
| 设计师 | 浅绿色牛仔夹克 | light green denim jacket |
| PD/产品 | 浅青色衬衫 | light teal button-up shirt |
| 业务方 | 淡橄榄绿衬衫+深绿领带 | light olive shirt, dark green tie |
| 测试 | 浅薄荷绿上衣 | light mint green top |
| AI 机器人 | 白色/浅绿色机身 | white body with light green outline |

## 暗夜暖金主题服装替换表

使用暗夜暖金主题时，替换上方服装描述，外观特征不变。

| 角色 | 暗夜暖金主题服装 | Prompt 关键词（替换服装部分） |
|------|---------------|------|
| 后端开发 | 深棕色毛衣，琥珀金边 | dark brown sweater with amber trim |
| 前端开发 | 深炭色帽衫(hoodie) | dark charcoal hoodie |
| 设计师 | 暖珊瑚色上衣 | soft coral top |
| PD/产品 | 深棕色衬衫 | dark brown shirt |
| 业务方 | 深炭色衬衫+琥珀金领带 | dark charcoal shirt, amber gold tie |
| 测试 | 暖蜂蜜色上衣 | warm honey top |
| AI 机器人 | 深灰色机身，琥珀金光晕 | dark grey body with amber glow outline |

## 线条与质感

- **线条基底**: 铅笔手绘质感，线条粗细自然变化
- **上色方式**: 水彩渲染感，颜色有自然晕染边界，不是数字化的平涂
- **纸张质感**: 带有微妙的纸纹肌理感（cream/off-white）
- **不完美感**: 线条略有抖动和不规则，体现手绘温度
- **阴影**: 柔和浅淡的水彩阴影，不使用硬边投影

## 系列一致性保证方法

生成多张系列配图时，用以下方法保持角色外观一致：

1. **固定角色 Block**：从角色设定表的「Prompt 关键词」列直接复制对应角色的英文描述，作为固定 block 粘贴到每张图的 prompt 中，不要每次重新翻译
2. **固定风格 Block**：通用前缀（含色调浓度档位）在所有图中保持完全一致
3. **只变化内容**：每张图只修改 COMPOSITION、PROPS、LABELS 部分，角色描述和风格描述不动
4. **同批次生成**：系列图尽量在同一个会话中连续生成，避免跨会话风格漂移
