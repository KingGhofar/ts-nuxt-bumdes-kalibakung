<script setup lang="ts">
import { Search, Eye, Trash2, MapPin } from 'lucide-vue-next'
useHead({ title: 'Aspirasi Warga' })
const route = useRoute()
const toast = useToast()
const { ask } = useConfirm()
const q = ref(String(route.query.q ?? ''))
const status = ref('')
const kategori = ref('')
const page = ref(1)
watch([q, status, kategori], () => (page.value = 1))
const { data, refresh } = await useFetch<any>('/api/aspirasi', { query: { q, status, kategori, page } })
const tiket = (a: any) => `#ASP-${new Date(a.createdAt).getFullYear()}-${String(a.id).padStart(3, '0')}`

async function publik(a: any, v: boolean) {
  try { await $fetch(`/api/aspirasi/${a.id}`, { method: 'PUT', body: { publik: v } }); a.publik = v; toast.success(v ? 'Aspirasi ditampilkan di portal publik.' : 'Aspirasi disembunyikan dari publik.') }
  catch (e) { toast.error(e) }
}
async function hapus(a: any) {
  if (!(await ask('Hapus Aspirasi?', `Aspirasi ${tiket(a)} dari ${a.nama} akan dihapus permanen.`, 'Hapus', true))) return
  try { await $fetch(`/api/aspirasi/${a.id}`, { method: 'DELETE' }); toast.success('Aspirasi dihapus.'); refresh() }
  catch (e) { toast.error(e) }
}
</script>

<template>
  <div>
    <PageHeader title="Aspirasi Warga" subtitle="Kelola pesan dari warga dan publikasikan yang relevan ke portal transparansi publik." :crumbs="[{ label: 'Aspirasi Warga' }]" />

    <div v-if="data" class="grid grid-cols-2 gap-4 xl:grid-cols-4">
      <StatCard label="Total Masuk" :value="data.stat.total" tone="ink" note="Akumulasi aspirasi" />
      <StatCard label="Menunggu" :value="data.stat.menunggu" tone="amber" note="Perlu tinjauan admin" />
      <StatCard label="Diproses" :value="data.stat.diproses" note="Sedang ditindaklanjuti" />
      <StatCard label="Selesai" :value="data.stat.selesai" tone="green" note="Tuntas ditangani" />
    </div>

    <div class="card mt-6 flex flex-col gap-2 p-4 md:flex-row">
      <div class="relative flex-1">
        <Search class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
        <input v-model="q" class="input pl-9" placeholder="Cari nama pengirim atau kata kunci…" aria-label="Cari aspirasi">
      </div>
      <div class="grid grid-cols-2 gap-2 md:flex">
        <select v-model="status" class="input md:w-44" aria-label="Filter status">
          <option value="">Semua Status</option><option value="MENUNGGU">Menunggu</option><option value="DIPROSES">Diproses</option><option value="SELESAI">Selesai</option>
        </select>
        <select v-model="kategori" class="input md:w-52" aria-label="Filter kategori">
          <option value="">Semua Kategori</option><option v-for="k in KATEGORI_ASPIRASI" :key="k">{{ k }}</option>
        </select>
      </div>
    </div>

    <section class="card mt-4 overflow-hidden">
      <!-- Desktop -->
      <div class="hidden overflow-x-auto lg:block">
        <table class="w-full table-fixed">
          <colgroup><col class="w-32"><col class="w-44"><col class="w-48"><col><col class="w-32"><col class="w-32"><col class="w-24"><col class="w-28"></colgroup>
          <thead class="border-b border-line bg-slate-50">
            <tr><th class="th">Tiket ID</th><th class="th">Pengirim</th><th class="th">Kategori &amp; Dusun</th><th class="th">Ringkasan Pesan</th><th class="th">Tanggal</th><th class="th">Status</th><th class="th">Publik</th><th class="th text-right">Aksi</th></tr>
          </thead>
          <tbody class="divide-y divide-line">
            <tr v-for="a in data?.items" :key="a.id" class="hover:bg-slate-50/60">
              <td class="td whitespace-nowrap font-mono text-xs font-bold text-primary-hover">{{ tiket(a) }}</td>
              <td class="td truncate font-medium" :title="a.nama">{{ a.nama }}</td>
              <td class="td"><p class="truncate">{{ a.kategori }}</p><p class="truncate text-xs text-muted">{{ a.dusun || '—' }}</p></td>
              <td class="td"><p class="truncate text-slate-600" :title="a.pesan">{{ a.pesan }}</p></td>
              <td class="td whitespace-nowrap text-xs">{{ tanggal(a.createdAt) }}</td>
              <td class="td"><StatusBadge :status="a.status" /></td>
              <td class="td"><ToggleSwitch :model-value="a.publik" :label="`Publikasikan ${tiket(a)}`" @update:model-value="publik(a, $event)" /></td>
              <td class="td">
                <div class="flex justify-end">
                  <NuxtLink :to="`/aspirasi/${a.id}`" class="icon-btn" aria-label="Detail"><Eye class="size-4" /></NuxtLink>
                  <button class="icon-btn text-red-500 hover:bg-red-50 hover:text-red-600" aria-label="Hapus" @click="hapus(a)"><Trash2 class="size-4" /></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Mobile / tablet -->
      <ul class="divide-y divide-line lg:hidden">
        <li v-for="a in data?.items" :key="a.id">
          <NuxtLink :to="`/aspirasi/${a.id}`" class="block space-y-2 p-4 active:bg-slate-50">
            <div class="flex items-center justify-between gap-2">
              <span class="font-mono text-xs font-bold text-primary-hover">{{ tiket(a) }}</span>
              <StatusBadge :status="a.status" />
            </div>
            <p class="font-semibold">{{ a.nama }}</p>
            <p class="line-clamp-2 text-sm text-slate-600">{{ a.pesan }}</p>
            <p class="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted">
              <span>{{ a.kategori }}</span><span v-if="a.dusun" class="flex items-center gap-1"><MapPin class="size-3" /> {{ a.dusun }}</span><span>{{ tanggal(a.createdAt) }}</span>
            </p>
          </NuxtLink>
        </li>
      </ul>

      <p v-if="!data?.items.length" class="px-4 py-12 text-center text-sm text-muted">Belum ada aspirasi yang sesuai.</p>
      <Pager v-if="data?.total" v-model="page" :total="data.total" :size="data.size" label="data aspirasi" />
    </section>
  </div>
</template>
