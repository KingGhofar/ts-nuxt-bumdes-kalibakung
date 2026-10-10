<script setup lang="ts">
import { FilePlus2, Save } from 'lucide-vue-next'
const props = defineProps<{ initial?: any }>()
const emit = defineEmits<{ saved: [] }>()
const toast = useToast()
const now = new Date()
const f = reactive({
  bulan: props.initial?.bulan ?? now.getMonth() + 1,
  tahun: props.initial?.tahun ?? now.getFullYear(),
  totalPemasukan: props.initial?.totalPemasukan ?? 0,
  totalPengeluaran: props.initial?.totalPengeluaran ?? 0,
  keterangan: props.initial?.keterangan ?? '',
  fileLpj: props.initial?.fileLpj ?? null,
})
const saldo = computed(() => f.totalPemasukan - f.totalPengeluaran)
const busy = ref(false)

async function simpan() {
  busy.value = true
  try {
    await $fetch(props.initial ? `/api/laporan/${props.initial.id}` : '/api/laporan', { method: props.initial ? 'PUT' : 'POST', body: f })
    toast.success('Laporan berhasil disimpan.')
    emit('saved')
  } catch (e) { toast.error(e) } finally { busy.value = false }
}
</script>

<template>
  <form @submit.prevent="simpan">
    <SectionCard :title="initial ? 'Edit Laporan' : 'Form Input Laporan Baru'" subtitle="Tambahkan rekapitulasi buku kas dan dokumen lampiran" :icon="FilePlus2">
      <template #aside><span class="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-primary">● {{ initial ? 'Edit' : 'Entri Baru' }}</span></template>
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
        <div>
          <label class="label" for="bl">Pilih Bulan Periode <span class="text-red-500">*</span></label>
          <select id="bl" v-model.number="f.bulan" class="input"><option v-for="(b, i) in BULAN" :key="b" :value="i + 1">{{ b }}</option></select>
        </div>
        <div><label class="label" for="th">Tahun Anggaran <span class="text-red-500">*</span></label><input id="th" v-model.number="f.tahun" type="number" min="2000" max="2100" required class="input"></div>
        <div>
          <label class="label">Total Pemasukan Kas <span class="text-red-500">*</span></label>
          <RupiahInput v-model="f.totalPemasukan" />
          <p class="mt-1 text-xs text-muted">Akumulasi seluruh unit usaha desa</p>
        </div>
        <div>
          <label class="label">Total Pengeluaran Kas <span class="text-red-500">*</span></label>
          <RupiahInput v-model="f.totalPengeluaran" />
          <p class="mt-1 text-xs text-muted">Termasuk belanja operasional &amp; honor pengelola</p>
        </div>
        <div class="rounded-lg border border-line bg-slate-50 p-4 sm:col-span-2">
          <p class="text-xs text-muted">Saldo Bersih (otomatis)</p>
          <p class="text-lg font-bold" :class="saldo >= 0 ? 'text-emerald-700' : 'text-red-600'">{{ saldo >= 0 ? '+' : '' }}{{ rupiah(saldo) }}</p>
        </div>
        <div class="sm:col-span-2"><label class="label" for="kt">Keterangan / Catatan Rekapitulasi</label><textarea id="kt" v-model="f.keterangan" rows="3" class="input" placeholder="Contoh: Rekap pendapatan unit air bersih & retribusi Wisata Kalimus periode ini…" /></div>
        <div class="sm:col-span-2">
          <label class="label">Unggah File Dokumen LPJ (PDF/Excel) – Opsional</label>
          <FileDrop v-model="f.fileLpj" kind="lpj" accept=".pdf,.xls,.xlsx" hint="PDF / Excel, maksimal 10MB." />
        </div>
      </div>
      <div class="mt-6 flex flex-col-reverse gap-2 border-t border-line pt-5 sm:flex-row sm:justify-end">
        <NuxtLink to="/laporan-keuangan" class="btn-outline">Batal</NuxtLink>
        <button class="btn-primary" :disabled="busy"><Save class="size-4" /> Simpan Laporan</button>
      </div>
    </SectionCard>
  </form>
</template>
