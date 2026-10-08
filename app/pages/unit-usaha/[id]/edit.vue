<script setup lang="ts">
const id = useRoute().params.id
const { data: u } = await useFetch<any>(`/api/unit-usaha/${id}`)
useHead({ title: 'Edit Unit Usaha · BUMDes Maju Jaya' })
</script>

<template>
  <div v-if="u">
    <PageHeader title="Edit Unit Usaha" :subtitle="u.nama" :crumbs="[{ label: 'Unit Usaha', to: '/unit-usaha' }, { label: u.nama, to: `/unit-usaha/${u.id}` }, { label: 'Edit' }]" />
    <UnitForm :initial="u" @saved="navigateTo(`/unit-usaha/${u.id}`)" />
  </div>
</template>
