<script setup lang="ts">
const brand = useBrand()
await callOnce('brand', async () => {
  brand.value = await $fetch('/api/public/brand')
})
useHead({ titleTemplate: t => (t ? `${t} · ${brand.value.nama}` : brand.value.nama) })
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  <AppToast />
</template>
