<script setup lang="ts">
declare const input: unknown;
export const label = typeof input === "string" ? input : "";
</script>
<template><div>{{ label }}</div></template>
