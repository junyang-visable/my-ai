# V-Frontend-Monitor 监控能力清单

> 数据来源：Sunfire 租户 6（ICBU），文件夹 `V-Frontend-Monitor`
> 按 项目 × 错误类型 罗列现有监控与告警触发条件。

## 能力总览

覆盖 **3 个前端项目**，每个项目监控 **4 类错误**，共 12 项监控 + 12 条告警规则，均为 critical 级别、全部生效。

| 项目代号 | 对应前端项目      |
| -------- | ----------------- |
| Arise    | Homepage Frontend |
| Bamboo   | Product Editor    |
| Dolphin  | Search Frontend   |

## 统一触发逻辑

**告警条件**：某类错误的**总量，最近 5 分钟与过去 5 分钟的差值超过阈值** → 触发 critical 告警。

- 即**环比突增检测**：只有当错误量相比上一个 5 分钟明显突增时才告警；错误量一直平稳（无论高低）不会触发。
- 检测频率：每分钟一次。
- 通知渠道：以钉钉为主（Dolphin 的 SSR 错误为短信）。

## Arise（Homepage Frontend）

| 监控项         | 触发条件                                 | 通知                        | 查看链接                                                                                 |
| -------------- | ---------------------------------------- | --------------------------- | ---------------------------------------------------------------------------------------- |
| 白屏           | 总量（最近 5 分钟与过去 5 分钟差值）> 10 | 钉钉                        | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9886?crossTenant=true) |
| SSR 渲染错误   | 总量（最近 5 分钟与过去 5 分钟差值）> 10 | 钉钉                        | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9906?crossTenant=true) |
| 自定义业务错误 | 总量（最近 5 分钟与过去 5 分钟差值）> 5  | 钉钉                        | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9907?crossTenant=true) |
| 组件渲染错误   | 总量（最近 5 分钟与过去 5 分钟差值）> 20 | 钉钉（10 分钟内不重复提醒） | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9912?crossTenant=true) |

## Bamboo（Product Editor）

| 监控项                          | 触发条件                                    | 通知 | 查看链接                                                                                 |
| ------------------------------- | ------------------------------------------- | ---- | ---------------------------------------------------------------------------------------- |
| 白屏                            | 总量（最近 5 分钟与过去 5 分钟差值）> 10    | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9902?crossTenant=true) |
| SSR 渲染错误                    | 总量（最近 5 分钟与过去 5 分钟差值）> 10    | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9905?crossTenant=true) |
| 自定义业务错误（商品更新接口）※ | 总量（最近 5 分钟与**一周前同期**差值）> 50 | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9909?crossTenant=true) |
| 组件渲染错误                    | 总量（最近 5 分钟与过去 5 分钟差值）> 5     | 钉钉 | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9910?crossTenant=true) |

## Dolphin（Search Frontend）

| 监控项         | 触发条件                                 | 通知                        | 查看链接                                                                                 |
| -------------- | ---------------------------------------- | --------------------------- | ---------------------------------------------------------------------------------------- |
| 白屏           | 总量（最近 5 分钟与过去 5 分钟差值）> 80 | 钉钉（15 分钟内不重复提醒） | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9903?crossTenant=true) |
| SSR 渲染错误   | 总量（最近 5 分钟与过去 5 分钟差值）> 10 | **短信**                    | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9904?crossTenant=true) |
| 自定义业务错误 | 总量（最近 5 分钟与过去 5 分钟差值）> 20 | 钉钉                        | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9908?crossTenant=true) |
| 组件渲染错误   | 总量（最近 5 分钟与过去 5 分钟差值）> 5  | 钉钉                        | [查看数据](https://x.alibaba-inc.com/custom/6/product/preview/spm/9911?crossTenant=true) |

## 说明

- ※ **唯一例外**：Bamboo 的「自定义业务错误（商品更新接口）」对比基线是**一周前同期**（同比突增检测），触发逻辑为"最近 5 分钟比一周前同期多出 50 以上才告警"，与其余 11 条的环比口径不同。
- 全部监控项为 SPM 类型、处于生效状态；告警规则统一归属应用 `v-search-rec-data-process`。
- 通知渠道以钉钉为主，Dolphin 的 SSR 渲染错误为短信。
- 抑制窗口仅 2 条设置：Dolphin 白屏（15 分钟）、Arise 组件渲染错误（10 分钟），其余使用默认。
- 「查看链接」指向各监控项的 Sunfire 数据页（x.alibaba-inc.com，需内网登录后访问）。
