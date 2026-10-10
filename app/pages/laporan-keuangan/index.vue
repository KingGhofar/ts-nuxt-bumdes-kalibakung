<script setup lang="ts">
import { Plus, Download, Wallet, TrendingUp, TrendingDown, Search, Pencil, Trash2, FileText, Calendar } from 'lucide-vue-next'
useHead({ title: 'Laporan Keuangan' })
const toast = useToast()
const { ask } = useConfirm()
const tahun = ref(new Date().getFullYear())
const page = ref(1)
const q = ref('')
watch(tahun, () => (page.value = 1))
const { data, refresh } = await useFetch<any>('/api/laporan', { query: { tahun, page } })
const tahunList = computed(() => Array.from({ length: 5 }, (_, i) => new Date().getFullYear() - i))
// ponytail: cari periode di sisi klien (per halaman). Pindah ke server bila data > ratusan.
const items = computed(() => (data.value?.items ?? []).filter((l: any) => periode(l.bulan, l.tahun).toLowerCase().includes(q.value.toLowerCase())))
const saldo = (l: any) => l.totalPemasukan - l.totalPengeluaran

async function publikasi(l: any, v: boolean) {
  const p = periode(l.bulan, l.tahun)
  const ok = v
    ? await ask('Publikasikan Laporan?', `Laporan ${p} akan dapat dilihat oleh masyarakat di portal publik.`, 'Publikasikan')
    : await ask('Tarik dari Publik?', `Laporan ${p} akan disembunyikan dari portal publik (jadi Draft).`, 'Jadikan Draft')
  if (!ok) return
  try {
    await $fetch(`/api/laporan/${l.id}`, { method: 'PUT', body: { status: v ? 'PUBLIK' : 'DRAFT' } })
    l.status = v ? 'PUBLIK' : 'DRAFT'
    toast.success(v ? 'Laporan berhasil dipublikasikan.' : 'Laporan dijadikan Draft.')
  } catch (e) { toast.error(e) }
}
async function hapus(l: any) {
  if (!(await ask('Hapus Laporan?', `Laporan ${periode(l.bulan, l.tahun)} akan dihapus. Tindakan ini tidak dapat dibatalkan.`, 'Hapus', true))) return
  try { await $fetch(`/api/laporan/${l.id}`, { method: 'DELETE' }); toast.success('Laporan dihapus.'); refresh() }
  catch (e) { toast.error(e) }
}
</script>

<template>
  <div>
    <PageHeader title="Kelola Laporan Keuangan" subtitle="Input rekapitulasi kas bulanan dan unggah dokumen LPJ untuk transparansi warga." :crumbs="[{ label: 'Laporan Keuangan' }]">
      <a :href="`/api/laporan/export?tahun=${tahun}`" class="btn-outline"><Download class="size-4" /> Unduh Rekap</a>
      <NuxtLink to="/laporan-keuangan/tambah" class="btn-primary"><Plus class="size-4" /> Tambah Laporan Bulanan</NuxtLink>
    </PageHeader>

    <div v-if="data" class="grid grid-cols-1 gap-4 md:grid-cols-3">
      <StatCard label="Total Saldo Kas BUMDes" :value="rupiah(data.ringkasan.saldoKas)" :icon="Wallet" note="Akumulasi seluruh periode" />
      <StatCard :label="`Total Pendapatan ${tahun}`" :value="rupiah(data.ringkasan.pendapatan)" :icon="TrendingUp" tone="green" note="Akumulasi seluruh unit usaha" />
      <StatCard :label="`Total Pengeluaran ${tahun}`" :value="rupiah(data.ringkasan.pengeluaran)" :icon="TrendingDown" tone="red" note="Biaya operasional & belanja modal" />
    </div>

    <section class="card mt-6 overflow-hidden">
      <div class="flex flex-col gap-3 p-5 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 class="font-semibold">Rekap Buku Kas &amp; Laporan Bulanan</h2>
          <p class="text-xs text-muted">Daftar buku kas bulanan &amp; status publikasinya</p>
        </div>
        <div class="flex flex-col gap-2 sm:flex-row">
          <div class="relative">
            <Search class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
            <input v-model="q" class="input pl-9 sm:w-56" placeholder="Cari periode…" aria-label="Cari periode">
          </div>
          <select v-model.number="tahun" class="input sm:w-36" aria-label="Filter tahun"><option v-for="t in tahunList" :key="t" :value="t">Tahun {{ t }}</option></select>
        </div>
      </div>

      <!-- Desktop: tabel -->
      <div class="hidden overflow-x-auto md:block">
        <table class="w-full">
          <thead class="border-y border-line bg-slate-50">
            <tr><th class="th">Periode</th><th class="th">Pemasukan</th><th class="th">Pengeluaran</th><th class="th">Saldo Bersih</th><th class="th">File LPJ</th><th class="th">Publikasi</th><th class="th text-right">Aksi</th></tr>
          </thead>
          <tbody class="divide-y divide-line">
            <tr v-for="l in items" :key="l.id" class="hover:bg-slate-50/60">
              <td class="td whitespace-nowrap font-medium"><span class="flex items-center gap-2"><Calendar class="size-4 text-muted" /> {{ periode(l.bulan, l.tahun) }}</span></td>
              <td class="td whitespace-nowrap">{{ rupiah(l.totalPemasukan) }}</td>
              <td class="td whitespace-nowrap">{{ rupiah(l.totalPengeluaran) }}</td>
              <td class="td">
                <span class="whitespace-nowrap rounded-full px-2.5 py-1 text-xs font-semibold ring-1" :class="saldo(l) >= 0 ? 'bg-emerald-50 text-emerald-700 ring-emerald-200' : 'bg-red-50 text-red-700 ring-red-200'">
                  {{ saldo(l) >= 0 ? '+' : '' }}{{ rupiah(saldo(l)) }}
                </span>
              </td>
              <td class="td">
                <a v-if="l.fileLpj" :href="fileUrl(l.fileLpj)" target="_blank" class="inline-flex items-center gap-2 whitespace-nowrap rounded-lg border border-line px-3 py-1.5 text-xs font-medium hover:bg-slate-50">
                  <FileText class="size-4 text-red-500" /> LPJ-{{ BULAN[l.bulan - 1].slice(0, 3) }}-{{ l.tahun }} <Download class="size-3.5 text-muted" />
                </a>
                <span v-else class="text-xs text-muted">Belum diunggah</span>
              </td>
              <td class="td">
                <div class="flex items-center gap-2">
                  <ToggleSwitch :model-value="l.status === 'PUBLIK'" :label="`Publikasi ${periode(l.bulan, l.tahun)}`" @update:model-value="publikasi(l, $event)" />
                  <span class="text-xs font-semibold" :class="l.status === 'PUBLIK' ? 'text-emerald-600' : 'text-muted'">{{ l.status === 'PUBLIK' ? 'Tampil' : 'Draft' }}</span>
                </div>
              </td>
              <td class="td">
                <div class="flex justify-end">
                  <NuxtLink :to="`/laporan-keuangan/${l.id}/edit`" class="icon-btn" aria-label="Edit"><Pencil class="size-4" /></NuxtLink>
                  <button class="icon-btn text-red-500 hover:bg-red-50 hover:text-red-600" aria-label="Hapus" @click="hapus(l)"><Trash2 class="size-4" /></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Mobile: kartu -->
      <ul class="divide-y divide-line border-t border-line md:hidden">
        <li v-for="l in items" :key="l.id" class="space-y-3 p-4">
          <div class="flex items-center justify-between gap-2">
            <p class="flex items-center gap-2 font-semibold"><Calendar class="size-4 text-muted" /> {{ periode(l.bulan, l.tahun) }}</p>
            <StatusBadge :status="l.status" />
          </div>
          <dl class="grid grid-cols-2 gap-2 text-sm">
            <div><dt class="text-xs text-muted">Pemasukan</dt><dd class="font-medium">{{ rupiah(l.totalPemasukan) }}</dd></div>
            <div><dt class="text-xs text-muted">Pengeluaran</dt><dd class="font-medium">{{ rupiah(l.totalPengeluaran) }}</dd></div>
            <div class="col-span-2"><dt class="text-xs text-muted">Saldo Bersih</dt><dd class="font-bold" :class="saldo(l) >= 0 ? 'text-emerald-700' : 'text-red-600'">{{ saldo(l) >= 0 ? '+' : '' }}{{ rupiah(saldo(l)) }}</dd></div>
          </dl>
          <div class="flex items-center justify-between gap-2 border-t border-dashed border-line pt-3">
            <label class="flex items-center gap-2 text-xs font-semibold">
              <ToggleSwitch :model-value="l.status === 'PUBLIK'" :label="`Publikasi ${periode(l.bulan, l.tahun)}`" @update:model-value="publikasi(l, $event)" /> Publikasi
            </label>
            <div class="flex">
              <a v-if="l.fileLpj" :href="fileUrl(l.fileLpj)" target="_blank" class="icon-btn" aria-label="Unduh LPJ"><FileText class="size-4 text-red-500" /></a>
              <NuxtLink :to="`/laporan-keuangan/${l.id}/edit`" class="icon-btn" aria-label="Edit"><Pencil class="size-4" /></NuxtLink>
              <button class="icon-btn text-red-500" aria-label="Hapus" @click="hapus(l)"><Trash2 class="size-4" /></button>
            </div>
          </div>
        </li>
      </ul>

      <p v-if="!items.length" class="border-t border-line px-4 py-12 text-center text-sm text-muted">
        Belum ada laporan untuk tahun {{ tahun }}. <NuxtLink to="/laporan-keuangan/tambah" class="font-semibold text-primary">Tambah laporan →</NuxtLink>
      </p>
      <Pager v-if="data?.total" v-model="page" :total="data.total" :size="data.size" label="periode" />
    </section>
  </div>
</template>
