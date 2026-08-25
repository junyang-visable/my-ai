# 防谎报三件套（Anti-False-Reporting）

> 成本接近零，收益最大，建议第一批就上（11020757606 / 11020729209 / 11020456085）。
> 多篇文章独立踩到同一个坑：Agent 会通过**删断言、改测试预期、新建测试文件**来"通过"验证。
> 这三件套就是堵这三条路。

## 件一：角色信息隔离

用两个独立 sub-agent，各自上下文 reset：

- **Implementer（写实现）**：**不看 Rubric**。防止它为了通过特定用例而硬编码。
  只拿到需求 / 技术方案 / 代码上下文。
- **Evaluator（写验收）**：**不看技术方案**。防止被实现思路带偏。
  只拿到需求 / Rubric / 运行结果 / 证据。
- 可进一步用不同厂商的模型做 Maker–Checker，规避单模型的早停与自夸偏差（11020604944）。

对照本 kit：Implementer 用 `harness-coding` 技能，Evaluator 用 `harness-testing` 技能，
两者不共享会话上下文。

## 件二：RED 必须先跑红一次

在让 Agent 修复前，先证明这条测试**确实能失败**。

- 11020729209 的硬约束：冒烟集写死，且首条用例（TC-001）必须先失败——
  "验收器要先被证伪才配当裁判"。
- 落地：新增用例先在无实现/旧实现下跑一次，确认 RED；再进入实现-绿灯循环。
- 本 kit 用断言锁（lock-tests.py）冻结冒烟集函数体，防止"修测试凑绿"。

## 件三：提示词显式声明

给实现会话的 prompt 里必须写这一句（缺了它，11020456085 记录到模型会直接改单测或
新建测试文件绕过检查）：

> **"测试当前不应通过，禁止修改测试使其通过。你的任务是改实现代码让测试变绿；
> 若你认为测试本身有误，停下来说明理由，不要擅自修改测试。"**

## 配套：断言锁工作流

```bash
# 1) 冒烟集稳定后，记录基线（测试函数体的 SHA）
python3 .harness/feedback/lock-tests.py update

# 2) 每次 validate 会自动校验；也可手动：
python3 .harness/feedback/lock-tests.py verify   # 不符 exit 2

# 3) 确需改动冒烟测试时，二选一放行并留审计痕迹：
HARNESS_LOCK_BYPASS=1 python3 .harness/feedback/lock-tests.py verify
# 或在该测试函数上方加注释： // @lock-bypass 原因……，然后重新 update
```
