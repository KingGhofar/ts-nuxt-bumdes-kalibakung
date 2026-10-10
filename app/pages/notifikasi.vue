<script setup lang="ts">
import { Search, MessageSquareText, FileBarChart, Store, ShieldCheck, Bell, CheckCheck, BellRing, Clock } from 'lucide-vue-next'
useHead({ title: 'Notifikasi' })
const q = ref('')
const { data, refresh } = await useFetch<any>('/api/notifikasi', { query: { q } })
const style: Record<string, [any, string, string, string]> = {
  aspirasi: [MessageSquareText, 'bg-amber-50 text-amber-600', 'Aspirasi Warga', 'bg-amber-50 text-amber-800 ring-amber-200'],
  laporan: [FileBarChart, 'bg-emerald-50 text-emerald-600', 'Laporan Keuangan', 'bg-emerald-50 text-emerald-800 ring-emerald-200'],
  unit: [Store, 'bg-indigo-50 text-indigo-600', 'Unit Usaha', 'bg-indigo-50 text-indigo-800 ring-indigo-200'],
  audit: [ShieldCheck, 'bg-blue-50 text-blue-600', 'Sistem', 'bg-blue-50 text-blue-800 ring-blue-200'],
}
const s = (t: string) => style[t] ?? [Bell, 'bg-slate-100 text-slate-600', 'Sistem', 'bg-slate-100 text-slate-700 ring-slate-200']

async function bacaSemua() {
  await $fetch('/api/notifikasi/read-all', { method: 'POST' })
  await Promise.all([refresh(), refreshNuxtData('notif-count')])
}
</script>

<template>
  <div>
    <PageHeader title="Notifikasi Sistem" subtitle="Pemberitahuan aktivitas terbaru dan riwayat sistem." :crumbs="[{ label: 'Notifikasi' }]">
      <button class="btn-outline" :disabled="!data?.unread" @click="bacaSemua"><CheckCheck class="size-4 text-primary" /> Tandai Semua Dibaca</button>
    </PageHeader>

    <div class="card mb-4 flex flex-col gap-4 p-5 sm:flex-row sm:items-center">
      <span class="grid size-12 shrink-0 place-items-center rounded-full bg-blue-50 text-primary"><BellRing class="size-6" /></span>
      <div class="min-w-0 flex-1">
        <p class="flex flex-wrap items-center gap-2 font-semibold">{{ data?.unread ?? 0 }} Notifikasi Belum Dibaca
          <span v-if="data?.unread" class="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-semibold text-primary">Memerlukan Perhatian</span>
        </p>
        <p class="text-sm text-muted">Aktivitas aspirasi warga, publikasi laporan, dan perubahan unit usaha tercatat otomatis.</p>
      </div>
    </div>

    <div class="relative mb-4">
      <Search class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
      <input v-model="q" class="input pl-9" placeholder="Cari riwayat notifikasi…" aria-label="Cari notifikasi">
    </div>

    <div class="card divide-y divide-line overflow-hidden">
      <div v-for="n in data?.items" :key="n.id" class="relative flex gap-3 p-4 sm:gap-4 sm:p-5" :class="{ 'bg-blue-50/40': !n.dibaca }">
        <span v-if="!n.dibaca" class="absolute left-1.5 top-1/2 size-1.5 -translate-y-1/2 rounded-full bg-primary" aria-label="Belum dibaca" />
        <span class="grid size-10 shrink-0 place-items-center rounded-full sm:size-11" :class="s(n.tipe)[1]"><component :is="s(n.tipe)[0]" class="size-5" /></span>
        <div class="min-w-0 flex-1">
          <div class="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between sm:gap-3">
            <p class="flex flex-wrap items-center gap-2 font-semibold">{{ n.judul }}
              <span class="rounded-full px-2 py-0.5 text-[11px] font-semibold ring-1" :class="s(n.tipe)[3]">{{ s(n.tipe)[2] }}</span>
            </p>
            <span class="flex shrink-0 items-center gap-1 text-xs text-muted"><Clock class="size-3" /> {{ waktuLalu(n.createdAt) }}</span>
          </div>
          <p class="mt-1 break-words text-sm text-muted">{{ n.pesan }}</p>
        </div>
      </div>
      <p v-if="!data?.items.length" class="p-12 text-center text-sm text-muted">Tidak ada notifikasi.</p>
    </div>
  </div>
</template>
