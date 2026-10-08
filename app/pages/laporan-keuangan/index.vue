<script setup lang="ts">
import { Plus, Download, Wallet, TrendingUp, TrendingDown, Search, Pencil, Trash2, FileText, Calendar } from 'lucide-vue-next'
useHead({ title: 'Laporan Keuangan · BUMDes Maju Jaya' })
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
    <PageHeader title="Kelola Laporan Keuangan" subtitle="Input rekapitulasi kas bulanan BUMDes dan unggah dokumen LPJ untuk transparansi warga." :crumbs="[{ label: 'Laporan Keuangan' }]">
      <a :href="`/api/laporan/export?tahun=${tahun}`" class="btn-outline"><Download class="size-4" /> Unduh Rekap</a>
      <NuxtLink to="/laporan-keuangan/tambah" class="btn-primary"><Plus class="size-4" /> Tambah Laporan Bulanan</NuxtLink>
    </PageHeader>

    <div v-if="data" class="grid gap-4 md:grid-cols-3">
      <StatCard label="Total Saldo Kas BUMDes" :value="rupiah(data.ringkasan.saldoKas)" :icon="Wallet" note="Akumulasi seluruh periode" />
      <StatCard :label="`Total Pendapatan ${tahun}`" :value="rupiah(data.ringkasan.pendapatan)" :icon="TrendingUp" tone="green" note="Akumulasi unit PAM, Wisata & Alsintan" />
      <StatCard :label="`Total Pengeluaran ${tahun}`" :value="rupiah(data.ringkasan.pengeluaran)" :icon="TrendingDown" tone="red" note="Biaya operasional & belanja modal" />
    </div>

    <section class="card mt-6 overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-3 p-5">
        <div>
          <h2 class="font-semibold">Rekap Buku Kas &amp; Laporan Bulanan</h2>
          <p class="text-xs text-muted">Daftar buku kas yang telah diaudit &amp; siap diakses publik</p>
        </div>
        <div class="flex gap-2">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
            <input v-model="q" class="input w-56 pl-9" placeholder="Cari periode…" aria-label="Cari periode">
          </div>
          <select v-model.number="tahun" class="input w-32" aria-label="Filter tahun"><option v-for="t in tahunList" :key="t" :value="t">Tahun {{ t }}</option></select>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full min-w-[860px]">
          <thead class="border-y border-line bg-slate-50">
            <tr><th class="th">Periode</th><th class="th">Pemasukan</th><th class="th">Pengeluaran</th><th class="th">Saldo Bersih</th><th class="th">File Dokumen LPJ</th><th class="th">Status Publikasi</th><th class="th text-right">Aksi</th></tr>
          </thead>
          <tbody class="divide-y divide-line">
            <tr v-for="l in items" :key="l.id">
              <td class="td font-medium"><span class="flex items-center gap-2"><Calendar class="size-4 text-muted" /> {{ periode(l.bulan, l.tahun) }}</span></td>
              <td class="td">{{ rupiah(l.totalPemasukan) }}</td>
              <td class="td">{{ rupiah(l.totalPengeluaran) }}</td>
              <td class="td">
                <span class="rounded-full px-2.5 py-1 text-xs font-semibold ring-1"
                  :class="l.totalPemasukan >= l.totalPengeluaran ? 'bg-green-50 text-green-700 ring-green-200' : 'bg-red-50 text-red-700 ring-red-200'">
                  {{ l.totalPemasukan >= l.totalPengeluaran ? '+' : '' }}{{ rupiah(l.totalPemasukan - l.totalPengeluaran) }}
                </span>
              </td>
              <td class="td">
                <a v-if="l.fileLpj" :href="fileUrl(l.fileLpj)" target="_blank" class="inline-flex items-center gap-2 rounded-lg border border-line px-3 py-1.5 text-xs font-medium hover:bg-slate-50">
                  <FileText class="size-4 text-red-500" /> LPJ-{{ BULAN[l.bulan - 1].slice(0, 3) }}-{{ l.tahun }} <Download class="size-3.5 text-muted" />
                </a>
                <span v-else class="text-xs text-muted">Belum diunggah</span>
              </td>
              <td class="td">
                <div class="flex flex-col items-start gap-1">
                  <ToggleSwitch :model-value="l.status === 'PUBLIK'" :label="`Publikasi ${periode(l.bulan, l.tahun)}`" @update:model-value="publikasi(l, $event)" />
                  <span class="text-xs" :class="l.status === 'PUBLIK' ? 'font-semibold text-green-600' : 'text-muted'">{{ l.status === 'PUBLIK' ? 'Tampil' : 'Draft' }}</span>
                </div>
              </td>
              <td class="td">
                <div class="flex justify-end gap-1">
                  <NuxtLink :to="`/laporan-keuangan/${l.id}/edit`" class="rounded-lg p-2 text-muted hover:bg-slate-100" aria-label="Edit"><Pencil class="size-4" /></NuxtLink>
                  <button class="rounded-lg p-2 text-red-500 hover:bg-red-50" aria-label="Hapus" @click="hapus(l)"><Trash2 class="size-4" /></button>
                </div>
              </td>
            </tr>
            <tr v-if="!items.length"><td colspan="7" class="td py-10 text-center text-muted">Belum ada laporan untuk tahun {{ tahun }}.</td></tr>
          </tbody>
        </table>
      </div>
      <Pager v-if="data" v-model="page" :total="data.total" :size="data.size" label="periode" />
    </section>
  </div>
</template>
