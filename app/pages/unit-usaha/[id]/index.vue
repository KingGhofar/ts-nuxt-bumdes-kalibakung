<script setup lang="ts">
import { Pencil, Store, Phone, User } from 'lucide-vue-next'
const id = useRoute().params.id
const { data: u } = await useFetch<any>(`/api/unit-usaha/${id}`)
useHead({ title: () => `${u.value?.nama ?? 'Unit'} · BUMDes Maju Jaya` })
</script>

<template>
  <div v-if="u">
    <PageHeader :title="u.nama" :subtitle="u.kategori" :crumbs="[{ label: 'Unit Usaha', to: '/unit-usaha' }, { label: u.nama }]">
      <NuxtLink :to="`/unit-usaha/${u.id}/edit`" class="btn-primary"><Pencil class="size-4" /> Edit</NuxtLink>
    </PageHeader>
    <div class="grid gap-6 lg:grid-cols-3">
      <div class="card overflow-hidden lg:col-span-2">
        <div class="relative h-64 bg-gradient-to-br from-blue-100 to-slate-200">
          <img v-if="u.foto" :src="fileUrl(u.foto)" alt="" class="size-full object-cover">
          <Store v-else class="absolute inset-0 m-auto size-16 text-slate-400" />
        </div>
        <div class="p-6">
          <h2 class="font-semibold">Deskripsi</h2>
          <p class="mt-2 whitespace-pre-line text-sm text-muted">{{ u.deskripsi || '-' }}</p>
        </div>
      </div>
      <div class="card space-y-4 p-6 text-sm">
        <div><p class="text-muted">Status</p><StatusBadge :status="u.aktif ? 'SELESAI' : 'DRAFT'" class="mt-1" /><span class="ml-2">{{ u.aktif ? 'Aktif' : 'Nonaktif' }}</span></div>
        <div><p class="flex items-center gap-1.5 text-muted"><User class="size-3.5" /> Penanggung Jawab</p><p class="font-medium">{{ u.penanggungJawab }}</p></div>
        <div><p class="flex items-center gap-1.5 text-muted"><Phone class="size-3.5" /> Kontak</p><p class="font-medium">{{ u.kontak }}</p></div>
        <div v-if="u.metrikLabel"><p class="text-muted">{{ u.metrikLabel }}</p><p class="font-semibold text-primary">{{ u.metrikNilai }}</p></div>
        <div><p class="text-muted">Terdaftar</p><p class="font-medium">{{ tanggal(u.createdAt) }}</p></div>
      </div>
    </div>
  </div>
</template>
