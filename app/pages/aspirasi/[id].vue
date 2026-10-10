<script setup lang="ts">
import { Trash2, Phone, MapPin, Tag, Calendar, Save } from 'lucide-vue-next'
const id = useRoute().params.id
const toast = useToast()
const { ask } = useConfirm()
const { data: a } = await useFetch<any>(`/api/aspirasi/${id}`)
useHead({ title: 'Detail Aspirasi' })
const f = reactive({ status: a.value?.status ?? 'MENUNGGU', catatanInternal: a.value?.catatanInternal ?? '', publik: a.value?.publik ?? false })
const busy = ref(false)
const tiket = computed(() => a.value ? `#ASP-${new Date(a.value.createdAt).getFullYear()}-${String(a.value.id).padStart(3, '0')}` : '')

async function simpan() {
  busy.value = true
  try { await $fetch(`/api/aspirasi/${id}`, { method: 'PUT', body: f }); toast.success('Aspirasi berhasil diperbarui.') }
  catch (e) { toast.error(e) } finally { busy.value = false }
}
async function hapus() {
  if (!(await ask('Hapus Aspirasi?', 'Aspirasi ini akan dihapus permanen.', 'Hapus', true))) return
  try { await $fetch(`/api/aspirasi/${id}`, { method: 'DELETE' }); toast.success('Aspirasi dihapus.'); navigateTo('/aspirasi') }
  catch (e) { toast.error(e) }
}
</script>

<template>
  <div v-if="a">
    <PageHeader :title="`Aspirasi ${tiket}`" :subtitle="`Dari ${a.nama}`" :crumbs="[{ label: 'Aspirasi Warga', to: '/aspirasi' }, { label: tiket }]">
      <button class="btn-outline text-red-600" @click="hapus"><Trash2 class="size-4" /> Hapus</button>
    </PageHeader>
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <section class="card min-w-0 p-5 sm:p-6 lg:col-span-2">
        <div class="flex flex-wrap gap-x-5 gap-y-2 text-sm text-muted">
          <span class="flex items-center gap-1.5"><Tag class="size-4" /> {{ a.kategori }}</span>
          <span v-if="a.dusun" class="flex items-center gap-1.5"><MapPin class="size-4" /> {{ a.dusun }}</span>
          <a v-if="a.whatsapp" :href="`https://wa.me/${a.whatsapp.replace(/\D/g, '').replace(/^0/, '62')}`" target="_blank" rel="noopener" class="flex items-center gap-1.5 text-emerald-700 hover:underline"><Phone class="size-4" /> {{ a.whatsapp }}</a>
          <span class="flex items-center gap-1.5"><Calendar class="size-4" /> {{ tanggal(a.createdAt) }}</span>
        </div>
        <p class="mt-5 whitespace-pre-line break-words rounded-xl border border-line bg-slate-50 p-5 italic leading-relaxed text-slate-700">“{{ a.pesan }}”</p>
      </section>
      <form class="card space-y-5 self-start p-5 sm:p-6" @submit.prevent="simpan">
        <div>
          <label class="label" for="st">Status Tindak Lanjut</label>
          <select id="st" v-model="f.status" class="input"><option value="MENUNGGU">Menunggu</option><option value="DIPROSES">Diproses</option><option value="SELESAI">Selesai</option></select>
        </div>
        <div><label class="label" for="cat">Catatan Internal</label><textarea id="cat" v-model="f.catatanInternal" rows="4" class="input" placeholder="Hanya terlihat oleh admin…" /></div>
        <div class="flex items-center justify-between gap-3 rounded-lg border border-line bg-slate-50 p-3">
          <div><p class="text-sm font-medium">Tampilkan di Portal Publik</p><p class="text-xs text-muted">Nama, kategori &amp; pesan terlihat warga</p></div>
          <ToggleSwitch v-model="f.publik" label="Tampilkan di portal publik" />
        </div>
        <button class="btn-primary w-full" :disabled="busy"><Save class="size-4" /> Simpan Perubahan</button>
      </form>
    </div>
  </div>
</template>
