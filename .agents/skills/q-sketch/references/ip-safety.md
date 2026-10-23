# IP 触发词避坑指南

ImageGen 会检测知名 IP 角色特征组合，触发 IPInfringementSuspect 错误导致生成失败。以下为已验证的避坑规则。

## 高危触发词（避免使用）

- 角色名 + 标志性外貌：如 "Elsa + golden braid + blue dress"、"Anna + red braids + green dress"
- 职业/身份 + 标志性特征：如 "princess + platinum blonde braid + ice crown"、"ice queen + blue gown"
- 具体 IP 名称：Disney、Frozen、Marvel、Pokemon、Hello Kitty 等

## 安全替代策略

- 去掉角色名称，用通用外貌描述替代：`girl with golden hair in blue dress`（OK）vs `Elsa in blue dress`（高危）
- 混搭多个特征打破标志性组合：不要同时出现某个 IP 角色的 2 个以上标志特征
- 动物/宠物用通用品种描述：`cute orange tabby cat`（OK）vs `Garfield`（高危）
