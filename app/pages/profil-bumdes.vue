<script setup lang="ts">
import { Check, Landmark, Flag, Users, Eye, Globe, ExternalLink, ArrowLeftRight, Plus, Trash2, Clock, UserRound } from 'lucide-vue-next'
useHead({ title: 'Profil BUMDes' })
const toast = useToast()
const brand = useBrand()
const { data } = await useFetch<any>('/api/bumdes')

type P = { nama: string, jabatan: string, keterangan: string, foto: string | null }
const kosong = () => ({
  nama: '', tahunBerdiri: null as number | null, dasarHukum: '', email: '', telepon: '', alamat: '',
  deskripsi: '', visi: '', misi: '', logo: null as string | null, jamOperasional: '', pengurus: [] as P[],
})
const f = reactive(kosong())
function load() {
  Object.assign(f, kosong())
  if (!data.value) return
  for (const k of Object.keys(f) as (keyof typeof f)[]) if (k !== 'pengurus' && data.value[k] != null) (f as any)[k] = data.value[k]
  f.pengurus = (data.value.pengurus ?? []).map((p: any) => ({ nama: p.nama, jabatan: p.jabatan, keterangan: p.keterangan ?? '', foto: p.foto }))
}
load()
const busy = ref(false)

async function simpan() {
  busy.value = true
  try {
    await $fetch('/api/bumdes', { method: 'PUT', body: f })
    brand.value = { ...brand.value, nama: f.nama, logo: f.logo, alamat: f.alamat }
    toast.success('Profil BUMDes berhasil disimpan.')
  } catch (e) { toast.error(e) } finally { busy.value = false }
}
const tambahPengurus = () => f.pengurus.push({ nama: '', jabatan: '', keterangan: '', foto: null })
const portal = computed(() => (import.meta.client ? `${location.origin}/publik` : '/publik'))
</script>

<template>
  <form @submit.prevent="simpan">
    <PageHeader title="Kelola Profil BUMDes" subtitle="Perbarui identitas, visi-misi, dan struktur pengurus yang tampil di portal publik warga." :crumbs="[{ label: 'Profil BUMDes' }]">
      <button type="button" class="btn-outline" @click="load">Batal</button>
      <button class="btn-primary" :disabled="busy"><Check class="size-4" /> Simpan Perubahan</button>
    </PageHeader>

    <div class="mb-6 flex flex-col gap-3 rounded-xl border border-blue-200 bg-blue-50 p-4 sm:flex-row sm:items-center">
      <span class="grid size-10 shrink-0 place-items-center rounded-lg bg-blue-100 text-primary"><ArrowLeftRight class="size-5" /></span>
      <p class="flex-1 text-sm text-slate-700">Informasi profil ini otomatis tampil di <b>Portal Transparansi Publik {{ f.nama || 'BUMDes' }}</b>.</p>
    </div>

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div class="min-w-0 space-y-6 lg:col-span-2">
        <SectionCard title="Informasi Umum BUMDes" subtitle="Legalitas entitas, kontak resmi, dan alamat kantor." :icon="Landmark">
          <div class="mb-5 flex flex-col gap-4 rounded-xl border border-line bg-slate-50 p-4 sm:flex-row sm:items-center">
            <img v-if="f.logo" :src="fileUrl(f.logo)" alt="Logo" class="size-16 rounded-xl border border-line bg-white object-cover">
            <span v-else class="grid size-16 place-items-center rounded-xl border border-line bg-white"><Landmark class="size-7 text-primary" /></span>
            <div class="flex-1">
              <p class="text-sm font-semibold">Lambang Resmi BUMDes</p>
              <p class="text-xs text-muted">Format PNG, JPG, atau SVG dengan rasio 1:1 (Maksimal 2MB).</p>
            </div>
            <ImagePick v-model="f.logo" label="Ubah Logo BUMDes" />
          </div>
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
            <div><label class="label" for="nama">Nama BUMDes <span class="text-red-500">*</span></label><input id="nama" v-model="f.nama" required class="input"></div>
            <div><label class="label" for="th">Tahun Berdiri</label><input id="th" v-model.number="f.tahunBerdiri" type="number" min="1900" max="2100" class="input" placeholder="Contoh: 2019"></div>
            <div class="sm:col-span-2"><label class="label" for="dh">Dasar Hukum / Perdes &amp; SK Pengesahan</label><input id="dh" v-model="f.dasarHukum" class="input" placeholder="Contoh: Perdes No. ... Tahun ..."></div>
            <div><label class="label" for="em">Email Kontak Resmi</label><input id="em" v-model="f.email" type="email" class="input"></div>
            <div><label class="label" for="tel">Nomor Telepon / WhatsApp</label><input id="tel" v-model="f.telepon" type="tel" class="input"></div>
            <div class="sm:col-span-2"><label class="label" for="al">Alamat Lengkap Kantor Sekretariat</label><textarea id="al" v-model="f.alamat" rows="2" class="input" /></div>
            <div class="sm:col-span-2"><label class="label" for="ds">Deskripsi Singkat (Beranda Publik)</label><textarea id="ds" v-model="f.deskripsi" rows="2" class="input" placeholder="Kalimat pembuka di beranda portal publik" /></div>
          </div>
        </SectionCard>

        <SectionCard title="Visi &amp; Misi BUMDes" subtitle="Panduan arah strategis dan komitmen pembangunan ekonomi desa." :icon="Flag">
          <div class="space-y-5">
            <div>
              <div class="flex flex-wrap justify-between gap-2"><label class="label" for="vi">Visi Utama</label><span class="text-xs text-slate-400">Disorot di beranda publik</span></div>
              <textarea id="vi" v-model="f.visi" rows="3" class="input leading-relaxed" />
            </div>
            <div>
              <div class="flex flex-wrap justify-between gap-2"><label class="label" for="mi">Pernyataan Misi</label><span class="text-xs text-slate-400">Gunakan butir bernomor</span></div>
              <textarea id="mi" v-model="f.misi" rows="6" class="input leading-relaxed" placeholder="1. ...&#10;2. ..." />
            </div>
          </div>
        </SectionCard>
      </div>

      <div class="min-w-0 space-y-6">
        <SectionCard title="Struktur Pengurus Utama" subtitle="Tampil di bagan organisasi portal publik." :icon="Users">
          <div class="space-y-3">
            <p v-if="!f.pengurus.length" class="rounded-lg bg-slate-50 px-3 py-4 text-center text-sm text-muted">Belum ada pengurus. Tambahkan direktur, sekretaris, bendahara, dll.</p>
            <div v-for="(p, i) in f.pengurus" :key="i" class="rounded-xl border border-line p-3">
              <div class="flex items-start gap-3">
                <img v-if="p.foto" :src="fileUrl(p.foto)" alt="" class="size-12 shrink-0 rounded-full object-cover">
                <span v-else class="grid size-12 shrink-0 place-items-center rounded-full bg-slate-100 text-slate-400"><UserRound class="size-6" /></span>
                <div class="min-w-0 flex-1 space-y-2">
                  <input v-model="p.jabatan" required class="input py-1.5 text-xs font-semibold text-primary" placeholder="Jabatan (mis. Direktur)" :aria-label="`Jabatan pengurus ${i + 1}`">
                  <input v-model="p.nama" required class="input py-1.5 font-semibold" placeholder="Nama lengkap" :aria-label="`Nama pengurus ${i + 1}`">
                  <input v-model="p.keterangan" class="input py-1.5 text-xs" placeholder="Periode / No. SK" :aria-label="`Keterangan pengurus ${i + 1}`">
                </div>
              </div>
              <div class="mt-3 flex justify-end gap-2">
                <ImagePick v-model="p.foto" />
                <button type="button" class="icon-btn size-8 text-red-500 hover:bg-red-50 hover:text-red-600" aria-label="Hapus pengurus" @click="f.pengurus.splice(i, 1)"><Trash2 class="size-4" /></button>
              </div>
            </div>
            <button type="button" class="flex w-full items-center justify-center gap-2 rounded-xl border-2 border-dashed border-slate-300 py-3 text-sm font-semibold text-primary hover:bg-blue-50" @click="tambahPengurus">
              <Plus class="size-4" /> Tambah Posisi / Pengurus
            </button>
          </div>
        </SectionCard>

        <SectionCard title="Jam Operasional Kantor" subtitle="Satu baris per jadwal: Hari | Jam" :icon="Clock">
          <textarea v-model="f.jamOperasional" rows="4" wrap="off" class="input overflow-x-auto text-[13px]" aria-label="Jam operasional kantor" placeholder="Senin - Kamis | 08:00 - 15:30 WIB&#10;Jumat | 08:00 - 11:30 WIB&#10;Sabtu, Minggu & Libur | Tutup" />
        </SectionCard>

        <section class="card p-5 sm:p-6">
          <div class="flex items-center justify-between">
            <h2 class="flex items-center gap-2 font-semibold"><Eye class="size-4 text-primary" /> Tampilan Publik Live</h2>
            <span class="size-2.5 rounded-full bg-green-500" />
          </div>
          <p class="mt-2 text-sm text-muted">Halaman ini dapat diakses terbuka oleh seluruh warga desa.</p>
          <a :href="portal" target="_blank" class="mt-4 flex items-center gap-2 rounded-lg border border-line bg-slate-50 px-3 py-2.5 text-sm">
            <Globe class="size-4 shrink-0 text-muted" /><span class="min-w-0 flex-1 truncate font-mono font-semibold">{{ portal }}</span><ExternalLink class="size-4 shrink-0 text-primary" />
          </a>
        </section>
      </div>
    </div>

    <div class="sticky bottom-0 -mx-4 mt-6 flex justify-end gap-2 border-t border-line bg-white/95 px-4 py-3 backdrop-blur sm:hidden">
      <button type="button" class="btn-outline flex-1" @click="load">Batal</button>
      <button class="btn-primary flex-1" :disabled="busy">Simpan</button>
    </div>
  </form>
</template>
