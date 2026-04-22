# 04 — 组件库文档

## 文档格式说明

本仓库组件文档遵循统一条目结构，便于 AI 与人类检索：

1. **组件名称**（中英文）
2. **一句话用途**
3. **Props / Emits / Slots** 表格（类型与默认值与源码一致）
4. **用法示例**（可复制到页面或 Story）
5. **可访问性 / 已知限制**（如有）

新增或修改公共组件时，须同步更新本节对应条目。

---

## 示例条目：`VbButton`（请替换为真实组件名）

**用途**：主操作按钮，统一主色、加载态与禁用样式。

### Props

| propName | type | required | default | description |
|----------|------|----------|---------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'ghost'` | 否 | `'primary'` | 视觉变体 |
| `size` | `'sm' \| 'md' \| 'lg'` | 否 | `'md'` | 尺寸 |
| `loading` | `boolean` | 否 | `false` | 为 true 时显示加载图标并禁用点击 |
| `disabled` | `boolean` | 否 | `false` | 禁用 |
| `block` | `boolean` | 否 | `false` | 宽度 100% |

### Emits

| 事件名 | payload | 说明 |
|--------|---------|------|
| `click` | `MouseEvent` | 原生点击；`loading` 或 `disabled` 时不触发 |

### Slots

| 插槽名 | 说明 |
|--------|------|
| `default` | 按钮文案 |
| `icon` | 前置图标（可选） |

### Usage

```vue
<script setup lang="ts">
import { VbButton } from '@/components/VbButton.vue'
</script>

<template>
  <VbButton variant="primary" :loading="isSubmitting" @click="onSubmit">
    提交
  </VbButton>
</template>
```

### 可访问性

- [替换: 如 role="button"、键盘 Enter 触发等]

---

## 组件索引（维护表）

| 组件 | 路径 | 备注 |
|------|------|------|
| [替换] | [替换: @/components/...] | [替换] |

---

- 维护人：[替换]
- 最后更新：[替换: YYYY-MM-DD]
