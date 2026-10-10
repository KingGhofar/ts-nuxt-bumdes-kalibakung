<script setup lang="ts">
useHead({ title: 'Tambah Laporan' })
</script>

<template>
  <div>
    <PageHeader title="Tambah Laporan Bulanan" subtitle="Input rekapitulasi kas bulanan dan dokumen LPJ." :crumbs="[{ label: 'Laporan Keuangan', to: '/laporan-keuangan' }, { label: 'Tambah' }]" />
    <LaporanForm @saved="navigateTo('/laporan-keuangan')" />
  </div>
</template>
