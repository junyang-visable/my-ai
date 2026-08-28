# FE-1042 行为评测样例（模拟 PR diff 片段）

> 用途：验收 AC1（未防护 → Must Fix）与 AC2（守卫 → 不报）。
> 评测方式：子代理只读更新后的规则文件 + 本文件，逐片段输出判定。

## Snippet 1 — composable 顶层未防护 localStorage

```ts
// composables/useRecentSearch.ts
export function useRecentSearch() {
  const recent = ref(JSON.parse(localStorage.getItem('recent-search') || '[]'))
  return { recent }
}
```

## Snippet 2 — `<script setup>` 顶层未防护 window

```vue
<!-- components/SearchBar.vue -->
<script setup lang="ts">
const isDesktop = window.innerWidth >= 1024
</script>
```

## Snippet 3 — 可选链伪防护

```ts
// composables/useLocale.ts
export function useLocale(): string {
  return window?.navigator?.language || 'en'
}
```

## Snippet 4 — typeof 守卫

```ts
// composables/useStoredFlag.ts
export function useStoredFlag(): boolean {
  if (typeof window === 'undefined') return false
  return localStorage.getItem('flag') === '1'
}
```

## Snippet 5 — import.meta.client 守卫

```ts
// plugins/analytics.ts (Nuxt 3)
export default defineNuxtPlugin(() => {
  if (import.meta.client) {
    window.__analyticsReady = true
  }
})
```

## Snippet 6 — onMounted 内访问

```vue
<!-- components/Chart.vue -->
<script setup lang="ts">
onMounted(() => {
  window.addEventListener('resize', handleResize)
})
</script>
```

## Snippet 7 — `<ClientOnly>` 包裹

```vue
<!-- pages/index.vue -->
<template>
  <ClientOnly>
    <MapWidget />
    <template #fallback>
      <div class="map-skeleton" />
    </template>
  </ClientOnly>
</template>
```
