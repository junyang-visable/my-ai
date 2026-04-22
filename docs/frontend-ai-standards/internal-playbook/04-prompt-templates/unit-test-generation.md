# 单元测试生成 Prompt 模板

## 使用场景

为 Vue 组件、composable 或纯函数编写 **Vitest** 单元测试，配合 **Vue Test Utils** 挂载组件。适用于回归防护、重构前补测试、覆盖边界分支等。

---

## Prompt 模板

````markdown
## 上下文

- 测试栈：Vitest、Vue Test Utils、`@vue/test-utils`；Vue 3 + TypeScript；项目测试配置文件路径：`[替换：如 vitest.config.ts]`。
- 待测代码（请完整粘贴，含相关子组件 import 若影响挂载）：

```ts
// 或 .vue 单文件内容
[替换：粘贴组件 script + template 关键部分，或 composable / util 完整代码]
```

- 依赖说明：`[替换：使用的 Pinia store、vue-router、i18n、第三方 composable 等]`

## 任务

为上述代码编写单元测试，重点覆盖场景：

- `[替换：如：默认渲染、必填 Prop 缺失时的降级]`
- `[替换：如：点击按钮 emit 正确事件与 payload]`
- `[替换：如：异步数据加载成功后列表项数量]`
- `[替换：补充边界与错误场景]`

## 约束

1. 使用 Vitest 的 **`describe` / `it`（或 `test`）** 结构；**每个 `it` 只断言一类行为**，避免一个用例夹杂过多无关断言。
2. **Mock 外部依赖**：HTTP、全局 store、路由、`useI18n` 等应在测试中显式 mock，**不发起真实网络请求**；mock 粒度与项目现有测试一致。
3. **测试行为而非实现细节**：优先断言用户可见结果（DOM 文本、emit、回调调用），避免过度依赖内部 `ref` 名或私有函数调用（除非纯函数单元测试）。
4. 异步测试使用 `async/await` 与 `find`、`waitFor` 等稳定等待方式；禁止无意义的固定 `setTimeout`。
5. 文件命名与路径遵循项目惯例：`[替换：如 tests/unit/ 或 __tests__]`。

## 输出要求

1. **完整可运行的测试文件**，保存路径：`[替换：如 tests/unit/components/Foo.spec.ts]`。
2. 包含必要的 `import`、`mount`/`shallowMount` 选择与简短理由（一句话）。
3. 若需工厂函数或测试夹具（fixtures），可一并给出；最后列出 **未覆盖但值得后续补充** 的场景（若有）。
````

---

## 效果优化建议

- **粘贴最小可测单元**：组件过大时，指定「只测某 Props 组合 + 某按钮」可得到更可维护的测试。
- **与 CI 对齐**：在「上下文」注明 Node 版本或 Vitest 环境（happy-dom / jsdom），避免 `window` 相关 API 差异。
- **快照慎用**：仅在纯展示且变更少时使用；默认要求模型用具体断言代替大块快照。
- **Pinia**：使用 `createPinia` + `setActivePinia` 模式时，可要求模型按官方测试文档写法输出，避免过时 API。
