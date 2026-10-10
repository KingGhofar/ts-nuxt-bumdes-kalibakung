<script setup lang="ts">
useHead({ title: 'Tambah Unit Usaha' })
</script>

<template>
  <div>
    <PageHeader title="Tambah Unit Usaha" subtitle="Daftarkan unit usaha baru BUMDes." :crumbs="[{ label: 'Unit Usaha', to: '/unit-usaha' }, { label: 'Tambah' }]" />
    <UnitForm @saved="navigateTo('/unit-usaha')" />
  </div>
</template>
