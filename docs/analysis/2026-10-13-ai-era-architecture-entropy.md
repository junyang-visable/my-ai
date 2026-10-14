# AI 时代的架构熵治理：熵增为什么加速，以及六道防线

> 成文于 2026-10-13。语料来自 ATA 站内检索（关键词：架构熵、架构腐化/劣化、技术债、代码质量、AI 编程、认知负荷、架构治理），共精读 13 篇，全部附文末链接。文中 ATA 观点均标注来源；标注「推断/建议」的内容是本文作者的综合判断。

## TL;DR

1. **架构熵不会消失，但 AI 改变了它的增速。** 架构熵的本质是"理解和修改系统的成本随时间自发增长"；AI 把代码生产成本压到接近零，而理解成本一分没降，熵从"按行计息"变成"按秒计息"。（[Codex 陪聊员](https://ata.atatech.org/articles/11020780091?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）
2. **垮塌不是某个瞬间的崩溃，而是认知赤字越过临界点。** 代码总量陡峭上升、团队真正说得清的代码量基本持平，中间那块"能跑、在线上、但没人敢碰"的面积持续扩大——这是垮塌前的常态而非异常。（同上）
3. **旧安全网在同时失效。**"写代码很疼"曾是天然的架构约束力；人工评审被 5 倍生成速度击穿成盖章；"测试通过"这个兜底在 AI 循环里既当运动员又当裁判。（[Loop Engineering 冷水](https://ata.atatech.org/articles/12020671641?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）
4. **治理重心的答案不是"少用 AI"，而是把约束从"人的自觉"迁移到"系统的确定性"。** 规则要硬（可执行卡口）、规范要在代码产生那一刻到场（Skill/hook）、流程要工件化（可审计）、验收要证据化、减法必须由人显式发起、度量要常态化。下文展开为六道防线。
5. **AI 不会让糟糕的流程变好，只会让糟糕的流程暴露得更快。** 熵治理的地基（架构约束、验收标准、反馈回路）在 AI 之前就该建；AI 只是让它从"可以欠着"变成"立即爆炸"。（[高德 WebX 实践](https://ata.atatech.org/articles/11020792820?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

---

## 一、先对齐概念：架构熵到底是什么

**复杂度 = 任何让软件难于理解、难于修改的因素。** 这是 Ousterhout《A Philosophy of Software Design》的定义，也是 ATA 上多篇复杂度文章共同的原点。复杂系统有三个可观测症状：变更放大（改一处要动多处）、认知负荷（读懂一个模块要付出的心智）、未知的未知（你不知道改这个会不会炸）。（[DDD 的知与行](https://ata.atatech.org/articles/11000249472?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)、[警惕复杂度困局](https://ata.atatech.org/articles/11000178074?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

**熵的直观理解：** 物理熵是"系统自发走向无序"的趋势。架构熵就是：只要有人在上面持续开发，系统的无序度（理解和维护成本）就会自发上升，且不施加外力（治理）就永不下降。菜鸟架构月刊把它与"组织熵"并列为工程团队的两大慢性病：架构熵影响可维护性，组织熵让每个人的时间被跨团队沟通吃掉。（[菜鸟工程闭环治理](https://ata.atatech.org/articles/11000266681?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

两个关键细分，决定了治理对象：

| 概念 | 含义 | 与熵治理的关系 |
|---|---|---|
| 本质复杂度 | 问题域自带的复杂度（业务本身就这么复杂） | 无法消除，只能缩小问题域；不是治理对象 |
| 偶然复杂度 | 解决方案引入的复杂度（技术选型、架构、代码风格、历史妥协） | **熵治理的主战场**，理论上可以压到很低 |

（[对抗软件复杂度的战争](https://ata.atatech.org/articles/11000233250?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

还有一个反直觉但重要的事实：**软件是长出来的，不是建造出来的。** 淘宝从单体 PHP 长了四五代架构才到今天；架构师设计的不是结构，而是"基因"（约束与准则）。所以熵增不是"当初设计的人挖的坑"，而是每个参与者的每个决定都在贡献复杂度——这也意味着治理必须是持续过程，不是一次性重构。（[警惕复杂度困局](https://ata.atatech.org/articles/11000178074?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

## 二、AI 为什么让熵增速率上了一个数量级

这一章是全文的核心论断，六条机制，每条都有站内实践佐证。

### 1. 生产成本归零，理解成本一分没降

Dijkstra 的老话：代码行数应记为"花掉的行数"（lines spent），不是"产出的行数"（lines produced）——每一行都是负债，要有人读、有人改、有人在凌晨三点被它叫醒。过去这笔负债有个天然刹车：写三百行比复用三十行更疼，"懒"是一种架构约束力。AI 把刹车拆了：生成三百行和三十行的体感都是"等二十秒"，于是「先搜一圈是否已有」这个念头不再划算，仓库里出现第 6 个 DateUtil，每个只被一处调用、每个只覆盖自己的边界情况。（[Codex 陪聊员](https://ata.atatech.org/articles/11020780091?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

### 2. AI 只做加法，几乎从不做减法

AI 的目标是让"这一次请求"通过，不是让系统三年后还能改。它永远建议加参数、加分支、加 adapter、加 xxxV2，极少建议"这个类拆掉重写""这两个模块可以合并、顺手删八百行"。单次看每个决策都合理，累积五十次就得到一个洋葱：每层都是当时最省事的选择，合起来没有任何人设计过。**减法必须由人显式发起，因为没人会替你发起。**（同上）

### 3. 上下文窗口 ≠ 系统认知

AI 不知道那行"多余"的空判断是某次线上故障的墓碑，不知道这个字段为什么不能改名，不知道这段重复是刻意的解耦。它会贴心地"清理"掉墓碑代码，并在总结里说代码更简洁了。这类破坏最贵，因为 diff 干净合理，能过评审。顺带的推论：**项目记忆必须写进仓库**（AGENTS.md、决策记录、注释）——以前规范文档没人看是因为人会互相问，现在你不写下来，AI 就真的不知道。（同上）

### 4. 一致性崩坏：十人十种生成风格

大模型在不同对话里面对相似上下文会产出风格迥异的代码：今天策略模式明天 if-else 瀑布，今天自定义错误类型明天直接 throw 字符串。十个开发者拿着各自的 spec 生成再合并，代码库变成拼凑体。这是「Spec 驱动开发」批判文章指出的要害：**代码库一致性从来无法靠输入端文档保证，只能靠输出端约束。**（[我为什么不喜欢 Spec 驱动开发](https://ata.atatech.org/articles/11020591263?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

云智能稳定性前端的复盘给了真实样本：后端同学用 AI 写前端，默认答案是 Vite + Tailwind + lucide-react，而团队线上同时存在 Ice + Fusion、Umi + AntD 等多套历史栈——功能跑起来了，但"不敢合进代码库"。（[AI Native 回忆录](https://ata.atatech.org/articles/11020781302?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

### 5. 评审被击穿：从把关退化成盖章

代码生成速度涨了 5 倍，人的阅读速度没涨。diff 200 行时评审人逐行看、作者逐行答辩；diff 2000 行时看目录结构、扫命名、点 LGTM。更糟的是连作者都不是第一读者了——那一千五百行的第一个完整读者可能不存在。文中结论值得单独一行：**在 AI 编码时代，限制单次 diff 大小的收益比过去大得多，它是唯一能让评审重新生效的杠杆。**（[Codex 陪聊员](https://ata.atatech.org/articles/11020780091?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

### 6. 验证的数学困境：可靠性是累乘的

无人值守的 loop 里，"另一个 Agent 说没问题"不是证据。三个来源互证：

- **累乘效应**：5 步链路每步 95% 可靠，整体成功率只有约 77%；步数越多越趋近于零。（[Loop Engineering 冷水](https://ata.atatech.org/articles/12020671641?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）
- **用预测验证预测**：LLM 检查 LLM 本质上是概率模型验概率模型。高德 WebX 的代码评审 Agent Kensa 在自建基准上 Precision 46.4%、Recall 61.3%——离"可托付"还有明显距离，人工 CR 仍不能去掉。（[AI 写代码已不是瓶颈](https://ata.atatech.org/articles/11020792820?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）
- **测试通过 ≠ 代码正确**：loop 可以生成在所有现有测试下表现正确、但引入想象不到的性能退化、安全漏洞或架构劣化的代码——因为那些不在测试范围内，也不在 spec 范围内。（[Loop Engineering 冷水](https://ata.atatech.org/articles/12020671641?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

### 附：为什么"体感没变快"

阿姆达尔定律：写代码只占交付周期的约 1/4，把它提速 5 倍，整体周期只从 100% 缩到 80%；而代码量变大后联调更久、评审更慢、回归面更大，很多团队的真实交付速度不升反降。瓶颈从编码转移到了 Plan/Review/Test/Deploy 这些仍以"人的速度"运行的环节。（[Codex 陪聊员](https://ata.atatech.org/articles/11020780091?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)、[AI 写代码变快后](https://ata.atatech.org/articles/11020778466?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

### 债务飞轮：六条机制如何互相加强

```
理解力债务增长
    → 你看不懂 AI 生成的代码
        → review 变得痛苦且低效
            → 倾向于放弃 review（认知投降）
                → 更多未验证代码进入代码库
                    → 验证问题加剧
                        → 理解力债务进一步增长 ……
```

（[Loop Engineering 冷水](https://ata.atatech.org/articles/12020671641?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) 提出的"债务飞轮"，三个轮辐：理解力债务、验证不可靠、认知投降。）**推断：** 这个飞轮同样适用于团队级架构熵——个体认知投降汇总成团队的评审失效，评审失效让平行抽象和重复轮子大量入库，库越乱下一代 AI 生成越偏离既有规范，飞轮转速更快。

## 三、架构垮塌的形态与账单

**临界点的定义（推断）：** 当"没人敢碰的代码"占比超过团队的维护带宽，且新需求只能继续往洋葱上再裹一层时，系统进入垮塌通道。表症不是宕机，而是：改任何东西都高风险、需求排期虚高、老人靠记忆撑着、新人只能另起炉灶。

五种典型形态：

| 形态 | 样子 | AI 时代的催化方式 |
|---|---|---|
| 平行抽象 | 同一概念四种实现，取决于当初谁在跟 AI 聊 | 生成成本为零，"先搜先复用"不划算 |
| 依赖环与分层倒挂 | 方法参数越加越多、if-else 越嵌越深 | AI 只求"能跑"，从不主动调整结构（[ARCH-CHECK](https://ata.atatech.org/articles/12020778474?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)） |
| 隐性知识蒸发 | 故障墓碑、历史兼容分支被"顺手清理" | AI 上下文里没有这段历史 |
| 规范-代码漂移 | 注释/Spec 与实现不一致，反成下一轮生成的噪声源 | AI 爱把 ADR、PR 链接、思考过程写进注释；文档腐化被加速（同上、[Spec 批判](https://ata.atatech.org/articles/11020591263?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)） |
| 组织熵 | 跨团队耦合、同一领域概念散落七个子系统 | AI 提速后流程与职责模糊更显眼（[对抗复杂度](https://ata.atatech.org/articles/11000233250?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)、[WebX](https://ata.atatech.org/articles/11020792820?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)） |

**垮塌的账单有多贵**：蚂蚁合并部署 2.0 是一个六年技术债的真实偿还案例——35 个核心应用、上游 300+ 应用 500+ 改造点，花了一年半才完成下线；期间还要顶着大促扩容的强制 deadline。教训被总结成三分法：技术债分**可避免**（发现立即还）、**策略性**（必须显式登记、定偿还周期）、**无法预知**（上线时就要准备下线策略）。（[我们花了一年半还了一个六年多的技术债](https://ata.atatech.org/articles/12020356838?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

**推断：** AI 时代的"策略性技术债"出现了一个新品种——「对 AI 生成代码的未审查合并」。传统技术债至少知道坑在哪（"这里偷懒用了全表扫描"），这种债连欠条都没有：没人深入理解过那段代码。按秒计息的就是它。

## 四、六道防线：把治理从"人的自觉"迁移到"系统的确定性"

总览（后六节展开）：

| # | 防线 | 回答的问题 | 代表实践 |
|---|---|---|---|
| 1 | 规则要硬 | 架构约束如何不被"遗忘" | Architect.md + arch-check 依赖矩阵 + 构建期卡口 |
| 2 | 规范到场 | 规则如何在代码产生那一刻生效 | Skill / Plugin / hook / 项目记忆 |
| 3 | 工件化流程 | 人和 AI 的协作靠什么对齐 | intent → spec → plan → verification 工件链 + 门禁 |
| 4 | 验收证据化 | "看起来对"如何变成"被证明对" | 分层评测 + 确定性门禁 + 运行时证据 |
| 5 | 人做减法 | 谁来对抗只增不减的默认倾向 | 意图先行、diff 答辩制、定期还债 |
| 6 | 度量闭环 | 熵增如何被看见、被驱动下降 | 架构分、闭环度、技术债台账 |

### 防线 1：规则要硬——把架构约束变成确定性检查

核心逻辑：**文档是建议，hook 才是拦截。** AI 上下文再长也会注意力稀释（写着写着就忘了 CLAUDE.md 里的要求），所以能确定判断的规范必须下沉到机器可判定的层面。

- **架构规范的唯一真相源**：如 ANYI 的 Architect.md——按真实项目结构逐一定义分包职责边界，把"通用能力下沉 foundation、业务层只能向下调用、反向依赖即违规"固化成硬约束，并在 CLAUDE.md 中强制"编码前先读"。（[ARCH-CHECK](https://ata.atatech.org/articles/12020778474?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）
- **依赖方向矩阵进构建期**：facade/util/dal/integration/core/biz/bootstrap 各层允许依赖谁写成 YAML，Maven 插件在编译期扫描，违规即 fail，且报错信息直接附上"Step1/Step2 修复指引"——让 AI 拿到报错就知道下一步做什么。配套量化规则：方法参数 ≤5、方法体 ≤100 行、嵌套深度 ≤3、重复率 ≤10%、禁直接 new 线程池。（同上）
- **参照系**：Uncle Bob 的方案是 CRAP 分数、环复杂度卡质量，变异测试验测试硬度，多 Agent 流水线互相制约——共同点是"给 AI 套确定性约束，而不是靠提示词求它"。（同上）
- **Ultra 级样板**：支付宝组件化范式中，"上层可依赖下层、下层禁止反向依赖""跨组件只能走 API Bundle"直接由构建期卡口强制（违规无法编译），配合架构分扣分形成治理闭环；最终主干定制率从 16% 降到 0.96%，主端瘦身 47M。（[支付宝组件化范式](https://ata.atatech.org/articles/12020534512?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

> 判断标准（建议）：一条架构规范是否值得下沉为检查，看它能否被 lint/AST/schema 编译期判定。能判定的绝不留在"团队共识"层面。

### 防线 2：规范到场——在代码产生的那一刻生效

云智能稳定性前端团队的关键转折：课程培训、知识库、换平台三条路都失败后，他们把顺序倒了过来——**不是先要求人完成一个动作再期待代码合规，而是让规则在代码产生那一刻到场。** 载体是 Skill：命中场景时自动进入 AI 上下文。（[AI Native 回忆录](https://ata.atatech.org/articles/11020781302?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

Skill 的五维结构值得抄：**When**（何时加载）、**What**（按项目类型选型）、**Don't/Why**（禁则+原因——AI 需要知道为什么不能做）、**How**（最小可运行样板）、**Map**（去哪找补充能力）。他们沉淀的八条禁则每条都带历史原因（如"禁裸 fetch——拦截器、鉴权、错误码统一走 goc-request"）。

工程化配套：

- **Plugin 打包**：Skills + Commands + Agents + Hooks + MCP 一次装齐，避免"少装一环 AI 照样工作、只是产出悄悄走偏"的隐性失败。
- **hook 拦高危动作**：AI 调 `npm install` 直接阻断（PreToolUse）；项目级 eslint+tsc 在 pre-commit 自动阻断；深度规范审查在提 PR 前手动触发——检查分了层，各管各的。
- **同一个错误出现第二次，就应该写进系统**：第一次可归因于上下文不足；第二次还错，说明该沉淀成 CLAUDE.md、Skill、hook、review policy 或测试用例。（[AI 写代码变快后](https://ata.atatech.org/articles/11020778466?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）
- **场景边界白名单**：哪些允许 AI 生成（样板代码、单测、文档），哪些禁止（安全关键路径、核心算法、敏感数据）——这是团队规范的一部分，不是个人自由裁量。（[Spec 批判](https://ata.atatech.org/articles/11020591263?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

### 防线 3：工件化流程——让每次变更可审计、可回放

AI-native SDLC 的核心接口不是 Markdown 文件本身，而是"committed artifact"这个动作：工件进了版本控制，就同时成为下一阶段的输入、协作的接口、审计的证据。（[AI 写代码变快后](https://ata.atatech.org/articles/11020778466?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

工件链示例：`intent.md`（目标、影响面、不可碰的边界）→ `spec.md`（设计约束）→ `plan.md`（执行顺序与风险）→ `verification.md`（红灯用例→绿灯证据）→ `review.md`（影响范围收窄结论）→ `release.md` / `operations.md`（上线与观察）→ `state.json` 串起时间轴。

两个关键设计：

- **门禁绑定工件 SHA-256**：工件后续被改，之前的审批自动失效——防的是"上下文已经变了，流程还假装没有变"。
- **AI 不拥有最终批准权**：分支保护、CODEOWNERS、发布授权是人类门禁，不是低效遗产，而是责任边界。AI 可以把材料备好、把失败原因解释清，但合并与否、上线与否、是否接受风险由人判断。（同上；亦见 [Spec 批判](https://ata.atatech.org/articles/11020591263?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)："谁提交的代码谁负责，git blame 上不会写 AI 的名字"）

### 防线 4：验收证据化——"看起来对"必须变成"被证明对"

高德 WebX 的分层评测揭示了一个要害事实：**局部正确不会自然累加成整体正确**——L1（原子 API）Pass1 82.6%，L2（0→1 完整页面）首轮按 100% 完成标准验收是 0%。Agent 会用 API，不等于能把生命周期、事件、状态组合成可用页面。（[AI 写代码已不是瓶颈](https://ata.atatech.org/articles/11020792820?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

三层验收体系：

1. **细粒度确定性门禁**：能明确判断的规范下沉到 schema/AST/lint/专用规则，结果可定位、可修复。对所有 Agent 都适用的原则是："让 AI 注意代码质量"等于没说。
2. **运行时证据**：真机/真实环境操作、截图留痕、取得运行证据才能标记 verified，否则输出 blocked/fail。移动端如此，前端页面、接口行为同理——"逻辑上应该正确"不算数。
3. **评测集守护 AI 配置本身**：收集 20-50 个真实任务做成 eval suite，CLAUDE.md、Skill、hook、prompt、模型任何一项变更都跑回归——**现在要担心的不只是代码改坏系统，还有"配置改坏了 AI 的行为"**。（[AI 写代码变快后](https://ata.atatech.org/articles/11020778466?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

同时给 LLM-as-Judge 留好心理预期：Kensa 的 P/R 数据说明检查 Agent 自身也要被评测、误差要被标定，人工 CR 在现阶段不可移除。（[WebX](https://ata.atatech.org/articles/11020792820?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

### 防线 5：人做减法——判断力和责任感不外包

这一道防线的对象是工程师个体，也是六道里唯一无法被系统代劳的。（[Codex 陪聊员](https://ata.atatech.org/articles/11020780091?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) 给出的操作清单，全文最实操）：

- **意图先行**：动手前自己写三行——改什么、为什么改、哪里不能碰。写不出来说明还没想清楚，而"想清楚"是唯一最不该外包的部分。
- **一轮会话只干一件事，diff 控制在"能逐行答辩"的量级**：评审人问任意一行"为什么"，你能立刻回答。答不上来就是塞多了。
- **显式要求做减法**：AI 不会自己发起。三句可用提示——"优先复用，不要新建"（先给它现有抽象清单）；"不要新增文件，在现有结构里解决"；改完追问"这次改动里，有哪些代码现在可以删掉了？"
- **测试边界人定**：AI 写实现 + AI 写测试 + AI 判断通过 = 自己出题自己打勾；漏掉的边界恰好和实现漏掉的是同一批。实现可以让 AI 写，用例边界必须人定，断言至少自己读一遍。
- **讲不清就不提交**：提交前口述主路径、失败分支、边界在哪。今天省下的十分钟是三个月后某个人的一整个下午。
- **定期还 AI 债**：每个迭代留固定时间，专搜重复抽象，该合的合、该删的删——债现在是按秒计息的，这件事从"可选"变成了"必须"。

配套一个 AI 时代被放大的老问题——**复用悖论**：错误的抽象、错误的复用对系统的危害比面条代码大得多，因为面条代码至少松耦合、改动影响可见，而高度"复用"的一行改动会把你想改的 8 个场景连同没想到的 20 个一起改掉。判别标准是意图：真重复（意图相同、需同步变化）才消除；意外重复（碰巧一样、各自演化）应保留。DRY 要谨慎用，YAGNI 优先，三次原则（Rule of Three）做平衡点。（[复用是美好的还是邪恶的](https://ata.atatech.org/articles/11020302481?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

**推断：** AI 让"错误抽象"的生产速度也翻了倍——它太擅长立刻给出一层貌似通用的抽象了。防线 5 和防线 1 要配合使用：减法靠人，减下来的成果靠确定性规则锁住，否则下个迭代的 AI 又会长回来。

### 防线 6：度量闭环——熵必须被看见才能被治理

"无法度量就无法治理"。站内三套可借鉴的度量体系：

- **架构分 + 四指标**（支付宝组件化）：组件化率、主干定制率、包大小、架构分，用榜单驱动各业务域持续优化；配合构建期卡口实现"劣化可拦截、质量可度量"。（[支付宝组件化范式](https://ata.atatech.org/articles/12020534512?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）
- **工程闭环度**（菜鸟）：用"需求闭环率"（编码/测试/发布不跨团队）和"应用闭环率"（代码 80% 由本团队贡献）量化架构熵与组织熵；≥80% 为优秀。落地一年从 21 个优秀团队涨到 50 个，并验证了闭环率高的团队满意度更高。（[菜鸟工程闭环治理](https://ata.atatech.org/articles/11000266681?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）
- **技术债台账**：定期组织识别→分类（可避免/策略/无法预知）→公开登记→评估→定偿还周期；每个新方案上线时就写好它的下线策略。（[一年半还六年债](https://ata.atatech.org/articles/12020356838?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

再加一条文化底座：**让增加/降低复杂度的行为透明**，并持续激励消除复杂度的行为——即"软件道德观"：以交付高质量的软件中间产物为荣。（[对抗软件复杂度的战争](https://ata.atatech.org/articles/11000233250?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

## 五、分工边界：人、AI、确定性系统各守什么

高德 WebX 的总结足够凝练，直接作为本节骨架（[来源](https://ata.atatech.org/articles/11020792820?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）：

| 角色 | 职责 | 不做什么 |
|---|---|---|
| 人 | **定义什么是好、识别什么是坏、决定什么时候停**；架构选型、减法、还债、最终批准 | 不逐行盯 AI 干活，不做"只会点同意的审核者" |
| AI | 语义理解、代码生成与修复、材料准备、失败归因解释 | 不拥有最终批准权；不负责定标准 |
| 确定性系统 | 调度、状态流转、门禁拦截、证据采集与留痕 | 不做语义判断 |

云智能团队对"AI 全栈"的适用边界同样值得参考：标准中后台页面可以放给 AI 全流程；前后端联动需求要结对和更强评审；核心链路、性能、数据一致性仍由领域专家主导——**全栈的 ROI 必须算长期维护账，跨端实现的人往往不是长期维护的人。**（[AI Native 回忆录](https://ata.atatech.org/articles/11020781302?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）

对无人值守 loop 的态度（[Loop Engineering 冷水](https://ata.atatech.org/articles/12020671641?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）：适用于重复性、可验证的任务（依赖更新、测试修复）；上生产代码库之前先具备**可观测**（能看清 Agent 在 loop 里如何决策）与**约束**（CLAUDE.md/Skill 规范化行为），并且清楚认知投降的四个阶段——有选择地信任 → 模式匹配 review → 仪式化 review → 完全委托。人一旦可以不思考，就一定会不思考。

## 六、落地路线（建议）

> 本节是作者基于上述语料的综合建议，非任何一篇文章的原文结论；按团队现状裁剪。

**第一周（止血）：**

1. 写最小版 Architect.md / CLAUDE.md：构建命令、测试命令、目录边界、高频踩坑、"哪些地方不能动"。
2. 给仓库装上 lint + 架构规则（哪怕是依赖方向 + 方法参数数两条），并进 pre-commit。
3. 开始限制单 PR / 单会话 diff 大小——这是让评审重新生效的最大杠杆，且零成本。
4. 把最近一次踩的坑写进约束文件（"错误第二次进系统"从此刻开始计数）。

**第一个月（成体系）：**

5. 把高频规范沉淀成 Skill（按五维结构），先覆盖"新人最容易写错"的三个场景。
6. 加 hook：拦截高危操作（生产配置、凭证、冻结包），post-edit 自动 format + lint。
7. 攒 20 条真实任务做 eval 基线；同时盘点技术债入台账，标类型和偿还周期。
8. 立规矩：AI 生成代码的 Review Checklist 单列，测试覆盖要求高于手写代码。

**第一季度（闭环）：**

9. 上架构度量看板（哪怕是简化版：重复率、依赖违规数、单 PR diff 中位数、评审驳回率）。
10. 固定"还债迭代"节奏；每个新方案上线时写明下线策略。
11. AI 配置（Skill/hook/prompt/模型）变更纳入 CI 回归。
12. 复盘一次协作惯性：流程反复回溯、沟通多轮往返、职责模糊、单线程默认——这四项是 AI 端到端交付的最大阻力（[WebX](https://ata.atatech.org/articles/11020792820?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）。

## 七、边界与风险（本文论证的适用范围）

- **不要把六道防线读成"六件必做大事"。** 治理本身也是成本；防线 1/2 的每个检查项都应从真实事故或高频错误中来，"错误第二次进系统"就是天然的准入闸门。一次性铺开会制造新的偶然复杂度——讽刺的是那正是本文要治的病。
- **规范-文档漂移是所有防线的共同敌人。** Architect.md、Skill、CLAUDE.md 都是新的"需要维护的产物"，它们的 Review 与版本化要进正常研发流程，否则只是把文档腐化换了个时髦名字。（[Spec 批判](https://ata.atatech.org/articles/11020591263?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE)）
- **部分数据的口径限制**：Kensa 的 P/R、L2 的 0%、累乘 77% 都来自特定基准与任务集，不能直接外推为自己的团队数据；引用时取其"结构性结论"（局部正确不累加、概率验证不可托付、可靠性累乘），不要引用具体数字当预算。
- **本文未覆盖**：组织熵的组织设计解法（菜鸟团队规模升级、闭环度牵引）只点到为止；安全与合规视角（AI 生成代码的安全漏洞率更高）只有单篇提及，值得单独立文。

## 参考资料

AI 时代研发范式（2026 年，核心语料）：

1. [全员当上「Codex 陪聊员」之后：进度没快多少，代码却越来越乱](https://ata.atatech.org/articles/11020780091?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 熵增六机制的个体视角与操作清单
2. [AI 写代码变快后，真正堵住团队的可能不是代码](https://ata.atatech.org/articles/11020778466?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — AI-native SDLC 工件链与门禁设计
3. [AI 写代码已不是瓶颈：我们如何把研发变成可验收的异步交付](https://ata.atatech.org/articles/11020792820?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 高德 WebX 全链路 Harness、分层评测
4. [AI Native 回忆录：云智能稳定性前端 S1 实践复盘](https://ata.atatech.org/articles/11020781302?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — Skill/Plugin 规范到场、设计-前端分库协作
5. [AI 写代码越来越快，谁来守住章法？ARCH-CHECK 教会 AI 下一步做什么](https://ata.atatech.org/articles/12020778474?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 架构规则确定性化样板
6. [我为什么不喜欢「Spec 驱动开发」？](https://ata.atatech.org/articles/11020591263?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 输入端幻觉与隐性技术债
7. [拒绝焦虑——给 Loop Engineering 泼一盆冷水](https://ata.atatech.org/articles/12020671641?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 债务飞轮、认知投降四阶段

架构复杂度与技术债经典：

8. [警惕复杂度困局：关于软件复杂度的思考](https://ata.atatech.org/articles/11000178074?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 认知负荷/协同成本二维框架
9. [对抗软件复杂度的战争](https://ata.atatech.org/articles/11000233250?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 本质/偶然复杂度、组织与政治因素
10. [菜鸟工程闭环治理，降低架构熵和组织熵](https://ata.atatech.org/articles/11000266681?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 熵的数字化度量
11. [我们花了一年半还了一个六年多的技术债](https://ata.atatech.org/articles/12020356838?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 技术债三分法与偿还流程
12. [架构设计的悖论，复用是美好的还是邪恶的](https://ata.atatech.org/articles/11020302481?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 真假重复、DRY 的克制使用
13. [支付宝超级App架构演进实践：构建面向未来的支付宝组件化范式](https://ata.atatech.org/articles/12020534512?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE) — 构建期卡口与架构度量闭环
