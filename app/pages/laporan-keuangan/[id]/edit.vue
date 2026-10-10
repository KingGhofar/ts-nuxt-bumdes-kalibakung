<script setup lang="ts">
const id = useRoute().params.id
const { data: l } = await useFetch<any>(`/api/laporan/${id}`)
useHead({ title: 'Edit Laporan' })
</script>

<template>
  <div v-if="l">
    <PageHeader title="Edit Laporan" :subtitle="periode(l.bulan, l.tahun)" :crumbs="[{ label: 'Laporan Keuangan', to: '/laporan-keuangan' }, { label: periode(l.bulan, l.tahun) }]" />
    <LaporanForm :initial="l" @saved="navigateTo('/laporan-keuangan')" />
  </div>
</template>
