<script setup lang="ts">
import { Search, Inbox, Clock, Loader, CheckCircle2, Eye, Globe } from 'lucide-vue-next'
useHead({ title: 'Aspirasi Warga · BUMDes Maju Jaya' })
const route = useRoute()
const q = ref(String(route.query.q ?? ''))
const status = ref('')
const kategori = ref('')
const page = ref(1)
watch([q, status, kategori], () => (page.value = 1))
const { data } = await useFetch<any>('/api/aspirasi', { query: { q, status, kategori, page } })
</script>

<template>
  <div>
    <PageHeader title="Aspirasi Warga" subtitle="Kelola masukan, saran, dan kendala yang disampaikan warga." :crumbs="[{ label: 'Aspirasi Warga' }]" />

    <div v-if="data" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <StatCard label="Total Aspirasi" :value="data.stat.total" :icon="Inbox" note="Akumulasi aspirasi masuk" />
      <StatCard label="Menunggu" :value="data.stat.menunggu" :icon="Clock" tone="amber" note="Perlu tinjauan admin" />
      <StatCard label="Diproses" :value="data.stat.diproses" :icon="Loader" note="Tindak lanjut unit usaha" />
      <StatCard label="Selesai" :value="data.stat.selesai" :icon="CheckCircle2" tone="green" note="Tuntas & arsip publik" />
    </div>

    <section class="card mt-6 overflow-hidden">
      <div class="flex flex-wrap gap-2 p-5">
        <div class="relative min-w-60 flex-1">
          <Search class="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
          <input v-model="q" class="input pl-9" placeholder="Cari nama pengirim atau kata kunci…" aria-label="Cari aspirasi">
        </div>
        <select v-model="status" class="input w-44" aria-label="Filter status">
          <option value="">Semua Status</option><option value="MENUNGGU">Menunggu</option><option value="DIPROSES">Diproses</option><option value="SELESAI">Selesai</option>
        </select>
        <select v-model="kategori" class="input w-52" aria-label="Filter kategori">
          <option value="">Semua Kategori</option><option v-for="k in KATEGORI_ASPIRASI" :key="k">{{ k }}</option>
        </select>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full min-w-[900px]">
          <thead class="border-y border-line bg-slate-50">
            <tr><th class="th">Pengirim</th><th class="th">Kategori</th><th class="th">Pesan</th><th class="th">Tanggal</th><th class="th">Status</th><th class="th">Publik</th><th class="th text-right">Aksi</th></tr>
          </thead>
          <tbody class="divide-y divide-line">
            <tr v-for="a in data?.items" :key="a.id">
              <td class="td"><p class="font-medium">{{ a.nama }}</p><p class="text-xs text-muted">{{ a.dusun }}</p></td>
              <td class="td">{{ a.kategori }}</td>
              <td class="td max-w-xs"><p class="line-clamp-2 text-muted">{{ a.pesan }}</p></td>
              <td class="td whitespace-nowrap">{{ tanggal(a.createdAt) }}</td>
              <td class="td"><StatusBadge :status="a.status" /></td>
              <td class="td"><Globe v-if="a.publik" class="size-4 text-green-600" aria-label="Publik" /><span v-else class="text-xs text-muted">—</span></td>
              <td class="td text-right"><NuxtLink :to="`/aspirasi/${a.id}`" class="btn-outline px-3 py-1.5"><Eye class="size-4" /> Detail</NuxtLink></td>
            </tr>
            <tr v-if="!data?.items.length"><td colspan="7" class="td py-10 text-center text-muted">Tidak ada aspirasi.</td></tr>
          </tbody>
        </table>
      </div>
      <Pager v-if="data" v-model="page" :total="data.total" :size="data.size" label="aspirasi" />
    </section>
  </div>
</template>
