<script setup lang="ts">
import { Search, MessageSquareText, FileBarChart, Store, ShieldCheck, Bell, CheckCheck } from 'lucide-vue-next'
useHead({ title: 'Notifikasi · BUMDes Maju Jaya' })
const q = ref('')
const { data, refresh } = await useFetch<any>('/api/notifikasi', { query: { q } })
const icons: Record<string, any> = { aspirasi: MessageSquareText, laporan: FileBarChart, unit: Store, audit: ShieldCheck }

async function bacaSemua() {
  await $fetch('/api/notifikasi/read-all', { method: 'POST' })
  await Promise.all([refresh(), refreshNuxtData('notif-count')])
}
</script>

<template>
  <div>
    <PageHeader title="Notifikasi Sistem" subtitle="Riwayat aktivitas dan log sistem." :crumbs="[{ label: 'Notifikasi' }]">
      <button class="btn-outline" :disabled="!data?.unread" @click="bacaSemua"><CheckCheck class="size-4" /> Tandai semua dibaca</button>
    </PageHeader>
    <div class="relative mb-4 max-w-md">
      <Search class="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
      <input v-model="q" class="input pl-9" placeholder="Cari riwayat notifikasi, log audit…" aria-label="Cari notifikasi">
    </div>
    <div class="card divide-y divide-line">
      <div v-for="n in data?.items" :key="n.id" class="flex gap-4 p-5" :class="{ 'bg-blue-50/50': !n.dibaca }">
        <span class="grid size-10 shrink-0 place-items-center rounded-full bg-blue-50 text-primary"><component :is="icons[n.tipe] ?? Bell" class="size-5" /></span>
        <div class="flex-1">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <p class="font-semibold">{{ n.judul }}</p>
            <span class="text-xs text-muted">{{ waktuLalu(n.createdAt) }}</span>
          </div>
          <p class="mt-1 text-sm text-muted">{{ n.pesan }}</p>
        </div>
        <span v-if="!n.dibaca" class="mt-2 size-2 shrink-0 rounded-full bg-primary" aria-label="Belum dibaca" />
      </div>
      <p v-if="!data?.items.length" class="p-10 text-center text-sm text-muted">Tidak ada notifikasi.</p>
    </div>
  </div>
</template>
