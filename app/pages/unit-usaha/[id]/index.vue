<script setup lang="ts">
import { Pencil, Store, Phone, User, CalendarDays } from 'lucide-vue-next'
const id = useRoute().params.id
const { data: u } = await useFetch<any>(`/api/unit-usaha/${id}`)
useHead({ title: () => u.value?.nama ?? 'Unit Usaha' })
</script>

<template>
  <div v-if="u">
    <PageHeader :title="u.nama" :subtitle="u.kategori" :crumbs="[{ label: 'Unit Usaha', to: '/unit-usaha' }, { label: u.nama }]">
      <NuxtLink :to="`/unit-usaha/${u.id}/edit`" class="btn-primary"><Pencil class="size-4" /> Edit</NuxtLink>
    </PageHeader>
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div class="card overflow-hidden lg:col-span-2">
        <div class="relative aspect-video bg-gradient-to-br from-sky-200 to-blue-100">
          <img v-if="u.foto" :src="fileUrl(u.foto)" alt="" class="size-full object-cover">
          <Store v-else class="absolute inset-0 m-auto size-16 text-white/80" />
        </div>
        <div class="p-5 sm:p-6">
          <h2 class="font-semibold">Deskripsi</h2>
          <p class="mt-2 whitespace-pre-line text-sm text-muted">{{ u.deskripsi || '—' }}</p>
        </div>
      </div>
      <dl class="card space-y-4 self-start p-5 text-sm sm:p-6">
        <div><dt class="text-muted">Status</dt><dd class="mt-1"><StatusBadge :status="u.aktif ? 'PUBLIK' : 'DRAFT'" /></dd></div>
        <div><dt class="flex items-center gap-1.5 text-muted"><User class="size-3.5" /> Penanggung Jawab</dt><dd class="font-medium">{{ u.penanggungJawab || '—' }}</dd></div>
        <div><dt class="flex items-center gap-1.5 text-muted"><Phone class="size-3.5" /> Kontak</dt><dd class="font-medium">{{ u.kontak || '—' }}</dd></div>
        <div v-if="u.metrikLabel"><dt class="text-muted">{{ u.metrikLabel }}</dt><dd class="font-semibold text-primary">{{ u.metrikNilai }}</dd></div>
        <div><dt class="flex items-center gap-1.5 text-muted"><CalendarDays class="size-3.5" /> Terdaftar</dt><dd class="font-medium">{{ tanggal(u.createdAt) }}</dd></div>
      </dl>
    </div>
  </div>
</template>
