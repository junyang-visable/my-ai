# Visable 商品优化 Skill

诊断并优化 wlw/Europages 商品信息 —— 标题、描述和商品属性。

**批量处理：** 支持可配置的批量扫描（默认 50 条，最大 200 条）。诊断、属性提取、内容优化、更新推送全部并行处理，不逐条轮询。

作者：David

---

## 目录结构

```
visable-product-opt/
├── SKILL.md                              # 主入口 —— 工作流、MCP 工具、分页逻辑
├── display.txt                           # Skill 元数据（名称、图标、版本）
├── README.md                             # 英文文档
├── README-CN.md                          # 本文档（中文）
└── reference/
    ├── quality-checker.md                # 诊断规则（标题、描述、属性、图片、更新时间、价格/起订量）
    ├── content-optimizer.md              # 标题 & 描述优化 prompt（硬约束）
    └── product-structure.md              # 商品 JSON 字段映射 & 编辑链接格式
```

### 文件职责

| 文件 | 职责 |
|------|------|
| `SKILL.md` | 流程编排：批量分页 → 并行诊断 → 并行属性提取 → 批量优化 → 确认 → 并行更新 |
| `quality-checker.md` | 诊断规则（标题、描述、属性、图片、更新时间、价格/起订量） |
| `content-optimizer.md` | 标题和描述两套独立 prompt，含硬过滤、仅基于事实、内容净化 |
| `product-structure.md` | 商品 JSON 字段到诊断变量的映射；ep/wlw 编辑链接格式 |

---

## 工作流程图

```mermaid
flowchart LR
    A([开始]):::se --> C[1 拉取批次]:::fet --> D[2 并行诊断]:::dia

    D --> E{有问题?}:::dec
    E -- 没有 --> F{还有更多?}:::dec
    F -- 是 --> C
    F -- 否 --> G([全部正常]):::ok

    E -- 有 --> H[3 并行提取属性]:::pv --> I[4 生成优化内容]:::opt --> J[5 展示报告]:::rpt

    J --> K{6 更新哪些字段?}:::dec
    K -- "标题/描述/属性" --> L[7 并行推送更新]:::upd --> M{8 继续?}:::dec
    K -- 跳过 --> M

    M -- 是 --> C
    M -- 否 --> N([结束]):::se

    classDef se fill:#6C757D,color:#fff,stroke:#495057
    classDef fet fill:#6610F2,color:#fff,stroke:#520DC2
    classDef dia fill:#D63384,color:#fff,stroke:#AB296A
    classDef dec fill:#FFC107,color:#000,stroke:#E0A800
    classDef pv fill:#20C997,color:#fff,stroke:#1AA179
    classDef opt fill:#0DCAF0,color:#000,stroke:#0AA2C0
    classDef rpt fill:#198754,color:#fff,stroke:#146C43
    classDef upd fill:#FD7E14,color:#fff,stroke:#CA6510
    classDef ok fill:#198754,color:#fff,stroke:#146C43
```

> 节点名称中的"并行"表示该步骤会同时处理多条商品，不逐条执行。

---

## 诊断规则总览

```mermaid
flowchart LR
    subgraph Title["标题检查"]
        style Title fill:#EBF5FB,stroke:#2E86C1,stroke-width:2px
        T1[不为空 ≥10字符]:::critical
        T2[核心产品词]:::critical
        T3[不堆砌关键词]:::high
        T4[拼写检查]:::high
    end

    subgraph Desc["描述检查"]
        style Desc fill:#FDF2E9,stroke:#E67E22,stroke-width:2px
        D1[最少100词]:::medium
        D2[不堆砌关键词]:::medium
        D3[无占位符文本]:::high
    end

    subgraph Info["其他检查"]
        style Info fill:#EAFAF1,stroke:#27AE60,stroke-width:2px
        P1[缺少属性]:::high
        P2[缺少图片]:::high
        P3[超180天未更新]:::medium
        P4[缺少价格]:::low
        P5[缺少起订量]:::low
    end

    Title --> Score
    Desc --> Score
    Info -.-> Score

    Score[/"检测问题\n报告给供应商"/]:::scoring

    classDef critical fill:#DC3545,color:#fff,stroke:#B02A37,stroke-width:2px
    classDef high fill:#FD7E14,color:#fff,stroke:#CA6510,stroke-width:2px
    classDef medium fill:#FFC107,color:#000,stroke:#E0A800,stroke-width:2px
    classDef low fill:#6C757D,color:#fff,stroke:#495057,stroke-width:1px
    classDef scoring fill:#6610F2,color:#fff,stroke:#520DC2,stroke-width:2px
```

---

## 交互时序图

```mermaid
sequenceDiagram
    autonumber
    actor U as 用户
    participant A as Agent
    participant API as MCP API

    rect rgb(235, 245, 251)
    Note over U,API: 第1轮 —— 触发 & 拉取
    U->>A: 帮我检查一下我的商品
    A->>API: visable_list_products(page=1, pageSize=50)
    API-->>A: 返回50条商品
    A->>A: 并行执行所有诊断规则
    A->>U: 第1批扫描完成：8条商品存在问题
    end

    rect rgb(253, 243, 226)
    Note over U,API: 第2轮 —— 诊断报告
    A->>API: visable_extract_pv（2条商品，并行调用）
    API-->>A: 返回建议属性
    A->>A: 批量生成优化标题和描述
    Note right of A: 报告包含：<br/>- 检测汇总<br/>- 超期未更新表<br/>- 缺图/缺价格/缺起订量表<br/>- 缺属性 + 建议属性<br/>- 标题问题 + 建议标题<br/>- 描述优化前后对比<br/>- 每行都有[编辑]链接
    A->>U: 发现8条有问题的商品<br/>需要我帮你更新到 Product Editor 吗？<br/>（标题/描述/属性，任选）
    end

    rect rgb(244, 236, 247)
    Note over U,API: 第3轮 —— 用户决策
    U->>A: 更新 #1 和 #2 的标题和属性，其他跳过
    A->>API: visable_update_product（#1 + #2，并行调用）
    API-->>A: 全部成功
    A->>U: 已更新2条（标题+属性），跳过6条<br/>还有85条商品待扫描<br/>要继续吗？
    end

    rect rgb(235, 245, 251)
    Note over U,API: 第4轮 —— 继续扫描
    U->>A: 继续
    A->>API: visable_list_products(page=2, pageSize=50)
    API-->>A: 返回50条商品
    A->>A: 50条全部正常 —— 自动扫描下一页
    A->>API: visable_list_products(page=3, pageSize=50)
    API-->>A: 返回35条商品（最后一页）
    A->>A: 发现2条有问题
    A->>U: 第3页发现2条问题商品<br/>需要我帮你更新到 Product Editor 吗？
    end

    rect rgb(234, 250, 241)
    Note over U,A: 第5轮 —— 结束
    U->>A: 不用了，结束吧
    A->>U: 最终汇总：<br/>共扫描135条，发现10个问题<br/>已更新2条，跳过8条，共3批
    end
```

---

## 完整对话示例

以下是一个完整的多轮对话示例，展示用户实际看到的内容。

---

**🧑 用户：**

> 帮我检查一下我的商品

**🤖 Agent：**

> 正在扫描您的商品目录... 第1批50条商品已加载，正在检查质量...
>
> 第1批扫描完成：发现 **6条** 商品存在问题。

**检测汇总：**

| 指标 | 数量 |
|------|------|
| 本批扫描商品 | 50 |
| 存在问题的商品 | 6 |
| 标题问题 | 2 |
| 描述问题 | 2 |
| 缺少属性 | 2 |
| 缺少图片 | 1 |
| 超过180天未更新 | 2 |
| 缺少价格 | 1 |
| 缺少起订量 | 1 |

**超过180天未更新的商品：**

| # | 商品标题 | 最后更新 | 操作 |
|---|---------|---------|------|
| 1 | Industrieventil DN50 | 2024-09-12 | [编辑](https://www.wlw.de/de/...) |
| 2 | Dichtungsring NBR | 2024-08-03 | [编辑](https://www.wlw.de/de/...) |

**缺少图片的商品：**

| # | 商品标题 | 操作 |
|---|---------|------|
| 1 | Stahlrohr nahtlos | [编辑](https://www.wlw.de/de/...) |

**缺少价格的商品：**

| # | 商品标题 | 操作 |
|---|---------|------|
| 1 | Trennscheibe 125 mm | [编辑](https://www.wlw.de/de/...) |

**缺少属性的商品（已自动提取建议属性）：**

| # | 商品标题 | 建议属性 | 操作 |
|---|---------|---------|------|
| 1 | Hydraulikpumpe | Material: Stahl, Gusseisen; Druck: 250 bar; Typ: Zahnradpumpe | [编辑](https://www.wlw.de/de/...) |
| 2 | Stahlrohr nahtlos | Material: Edelstahl, Kohlenstoffstahl; Durchmesser: 50 mm, 100 mm; Norm: DIN 2448 | [编辑](https://www.wlw.de/de/...) |

> 说明：同一属性有多个值时会合并展示，如 "Material: Edelstahl, Kohlenstoffstahl"。

**标题问题：**

| # | 当前标题 | 问题 | 建议标题 | 操作 |
|---|---------|------|---------|------|
| 1 | BEST Cutting Disc!! FREE SHIPPING | 含促销用语、特殊字符 | Trennscheibe - Stahl - 125 mm | [编辑](https://www.wlw.de/de/...) |
| 2 | Pumpe | 标题过短 | Hydraulikpumpe - Zahnradpumpe - 250 bar | [编辑](https://www.wlw.de/de/...) |

**描述优化详情：**

---

**商品 #1: [BEST Cutting Disc!! FREE SHIPPING](https://www.wlw.de/de/...)**

问题：含占位符文本，描述过短（23词，最低要求100词）

**当前描述：**
> coming soon, more details to follow...

**建议描述：**
> Die Trennscheibe eignet sich fuer den Einsatz bei Stahlwerkstoffen bis 5 mm Materialstaerke. Hohe Schnittleistung und lange Standzeit durch optimierte Kornmischung.
> - Durchmesser: 125 mm
> - Dicke: 1 mm
> - Max. Drehzahl: 12.250 U/min
> - Sicherheitsnorm: EN 12413

---

**商品 #2: [Pumpe](https://www.wlw.de/de/...)**

问题：描述过短（15词，最低要求100词），缺少技术细节

**当前描述：**
> Hochwertige Pumpe fuer industrielle Anwendungen. Kontaktieren Sie uns fuer Details.

**建议描述：**
> Die Hydraulikpumpe vom Typ Zahnradpumpe eignet sich fuer den Einsatz in hydraulischen Antriebssystemen mit einem Betriebsdruck von bis zu 250 bar.
> - Typ: Zahnradpumpe
> - Max. Betriebsdruck: 250 bar
> - Foerdervolumen: 20 l/min
> - Anschluss: G 1/2"

---

> **需要我帮你把这些建议直接更新到 Product Editor 后台吗？**
>
> 你可以选择更新哪些内容：
> - **标题** —— 应用建议的标题优化
> - **描述** —— 应用建议的描述优化
> - **属性** —— 应用提取的商品属性
>
> 可以任意组合，比如："全部更新"、"只更新 #1 和 #2 的标题和属性"、"只更新描述"。

---

**🧑 用户：**

> 更新 #1 和 #2 的标题和属性

**🤖 Agent：**

> 完成！已更新2条商品（标题 + 属性），跳过4条。
>
> 还有 **85条商品** 待扫描，需要我继续检查下一批吗？

---

**🧑 用户：**

> 继续

**🤖 Agent：**

> 正在扫描第2批（50条商品）... 全部正常，自动扫描第3批...
>
> 第3批扫描完成（35条商品，最后一页）：发现 **2条** 商品存在问题。
>
> *(展示第3批的报告...)*
>
> 需要我帮你更新到 Product Editor 后台吗？

---

**🧑 用户：**

> 不用了，结束吧

**🤖 Agent：**

> **最终汇总：**
>
> | 指标 | 数量 |
> |------|------|
> | 总扫描商品数 | 135 |
> | 总发现问题数 | 8 |
> | 已更新商品数 | 2 |
> | 跳过商品数 | 6 |
> | 扫描批次数 | 3 |
>
> 全部完成！您可以随时点击上方的 [编辑] 链接手动查看剩余商品。

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 批量并行处理 | 诊断、属性提取、内容生成、更新推送全部并行，不逐条轮询 |
| 可配置批量大小 | 默认50条，最大200条，用户可自定义 |
| 选择性检查 | 用户可指定只检查某些项（如"只查标题"、"只查属性"），跳过其他检查 |
| 字段粒度更新 | 标题、描述、属性三者任意组合更新，也可按行号选择特定商品 |
| 自动翻页 | 当前批次无问题时自动扫描下一批，直到发现问题或全部扫完 |
| 长描述友好展示 | 描述的优化前后对比不塞进表格，独立区块展示 |
| 属性多值合并 | 同一属性有多个值时合并为一行展示（如 Material: Stahl, Gusseisen） |
| 多语言支持 | 对话语言跟随用户，商品优化语言跟随商品本身的语言 |
