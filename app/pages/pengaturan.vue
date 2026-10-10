<script setup lang="ts">
import { BadgeCheck, KeyRound, ShieldCheck, UserRound, Bell, User, Mail, Briefcase, Phone, Fingerprint, Building2, Lock, Info, Save, RefreshCw } from 'lucide-vue-next'
useHead({ title: 'Pengaturan' })
const toast = useToast()
const route = useRoute()
const { fetchMe } = useAuth()
const brand = useBrand()
type Tab = 'profil' | 'keamanan' | 'notifikasi'
const tab = ref<Tab>(route.query.tab === 'keamanan' ? 'keamanan' : 'profil')
const { data: akun } = await useFetch<any>('/api/akun')
const kosong = () => ({ nama: '', email: '', jabatan: '', telepon: '', unitKerja: '', avatar: null as string | null })
const f = reactive(kosong())
function load() { Object.assign(f, kosong(), Object.fromEntries(Object.keys(f).map(k => [k, akun.value?.[k] ?? (k === 'avatar' ? null : '')]))) }
load()
const pw = reactive({ lama: '', baru: '', ulang: '' })
// ponytail: preferensi notifikasi disimpan di cookie browser saja. Pindah ke tabel bila perlu kirim email/WA sungguhan.
const pref = useCookie('notif-pref', { default: () => ({ aspirasi: true, laporan: true, email: false }) })
const busy = ref(false)
const initials = computed(() => f.nama.split(' ').map(s => s[0]).slice(0, 2).join('').toUpperCase() || '?')

async function simpanProfil() {
  busy.value = true
  try { await $fetch('/api/akun', { method: 'PUT', body: f }); await fetchMe(); toast.success('Profil akun berhasil disimpan.') }
  catch (e) { toast.error(e) } finally { busy.value = false }
}
async function gantiPw() {
  if (pw.baru !== pw.ulang) return toast.error('Konfirmasi password tidak sama.')
  busy.value = true
  try { await $fetch('/api/akun/password', { method: 'PUT', body: { lama: pw.lama, baru: pw.baru } }); Object.assign(pw, { lama: '', baru: '', ulang: '' }); toast.success('Password berhasil diubah.') }
  catch (e) { toast.error(e) } finally { busy.value = false }
}
const tabs = [['profil', 'Profil Akun', 'Profil', UserRound], ['keamanan', 'Keamanan & Autentikasi', 'Keamanan', ShieldCheck], ['notifikasi', 'Preferensi Notifikasi', 'Notifikasi', Bell]] as const
const fields = [
  ['nama', 'Nama Lengkap', User, 'text', true], ['email', 'Email Kedinasan', Mail, 'email', true],
  ['jabatan', 'Jabatan / Posisi', Briefcase, 'text', false], ['telepon', 'Nomor Telepon / WhatsApp', Phone, 'tel', false],
] as const
</script>

<template>
  <div>
    <PageHeader title="Pengaturan Sistem" subtitle="Konfigurasi akun admin dan preferensi aplikasi." :crumbs="[{ label: 'Pengaturan' }]">
      <span class="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-800"><BadgeCheck class="size-4" /> Status Akun: Aktif</span>
    </PageHeader>

    <div class="mb-6">
      <div class="grid grid-cols-3 border-b border-line sm:flex sm:gap-1" role="tablist">
        <button
          v-for="[k, l, s, ic] in tabs" :key="k" role="tab" :aria-selected="tab === k"
          class="flex items-center justify-center gap-2 border-b-2 px-2 py-3 text-sm font-medium transition sm:px-4"
          :class="tab === k ? 'border-primary text-primary' : 'border-transparent text-muted hover:text-ink'" @click="tab = k"
        ><component :is="ic" class="size-4 shrink-0" /> <span class="sm:hidden">{{ s }}</span><span class="hidden sm:inline">{{ l }}</span></button>
      </div>
    </div>

    <form v-if="tab === 'profil'" class="card overflow-hidden" @submit.prevent="simpanProfil">
      <div class="flex flex-col gap-4 border-b border-line bg-slate-50 p-5 sm:p-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 class="font-semibold">Pengaturan Profil Administrator</h2>
          <p class="text-sm text-muted">Kelola identitas kedinasan dan akses pengelola {{ brand.nama }}.</p>
        </div>
        <span class="inline-flex items-center gap-2 self-start rounded-lg border border-blue-200 bg-blue-50 px-3 py-2 text-xs text-slate-700"><RefreshCw class="size-4 text-primary" /> Nama &amp; jabatan dipakai di header admin</span>
      </div>

      <div class="space-y-6 p-5 sm:p-6">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center">
          <img v-if="f.avatar" :src="fileUrl(f.avatar)" alt="" class="size-20 rounded-full object-cover ring-4 ring-blue-100">
          <span v-else class="grid size-20 place-items-center rounded-full bg-indigo-100 text-xl font-bold text-primary ring-4 ring-blue-50">{{ initials }}</span>
          <div class="space-y-2">
            <p class="text-sm font-semibold">Foto Profil Administrator</p>
            <div class="flex gap-2">
              <ImagePick v-model="f.avatar" />
              <button v-if="f.avatar" type="button" class="btn px-2 py-1.5 text-xs text-red-600 hover:bg-red-50" @click="f.avatar = null">Hapus</button>
            </div>
            <p class="text-xs text-muted">Format JPG, PNG, atau SVG (Maks. 2MB). Rasio 1:1.</p>
          </div>
        </div>

        <div class="border-t border-line pt-6">
          <h3 class="font-semibold">Data Diri &amp; Penugasan</h3>
          <p class="text-xs text-muted">Data ini digunakan untuk pengesahan laporan dan audit keuangan.</p>
          <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2">
            <div v-for="[k, l, ic, t, req] in fields" :key="k">
              <label class="label" :for="k">{{ l }} <span v-if="req" class="text-red-500">*</span></label>
              <div class="relative">
                <component :is="ic" class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
                <input :id="k" v-model="f[k]" :type="t" :required="req" class="input pl-9" :placeholder="k === 'telepon' ? '08xx-xxxx-xxxx' : undefined">
              </div>
            </div>
            <div>
              <div class="flex justify-between gap-2"><label class="label" for="nik">NIK / Identitas Pegawai</label><span class="flex items-center gap-1 text-xs text-muted"><Lock class="size-3" /> Terkunci</span></div>
              <div class="relative">
                <Fingerprint class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
                <input id="nik" :value="akun?.nik ?? ''" readonly class="input pl-9" placeholder="Belum diisi">
              </div>
            </div>
            <div>
              <label class="label" for="uk">Unit Kerja Penugasan</label>
              <div class="relative">
                <Building2 class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
                <input id="uk" v-model="f.unitKerja" class="input pl-9" placeholder="Contoh: Kantor BUMDes">
              </div>
            </div>
          </div>
        </div>

        <div class="border-t border-line pt-6">
          <h3 class="font-semibold">Keamanan Ringkas</h3>
          <div class="mt-4 flex flex-col gap-4 rounded-xl border border-line p-4 sm:flex-row sm:items-center">
            <span class="grid size-10 shrink-0 place-items-center rounded-lg bg-blue-50 text-primary"><KeyRound class="size-5" /></span>
            <div class="flex-1"><p class="text-sm font-semibold">Kata Sandi Akun</p><p class="text-xs text-muted">Perbarui sandi secara berkala demi keamanan data keuangan desa.</p></div>
            <button type="button" class="btn-outline" @click="tab = 'keamanan'"><KeyRound class="size-4" /> Ganti Kata Sandi</button>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-3 border-t border-line bg-slate-50 p-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <p class="flex items-center gap-2 text-xs text-muted"><Info class="size-4 shrink-0 text-primary" /> Perubahan langsung berlaku di seluruh modul.</p>
        <div class="flex gap-2">
          <button type="button" class="btn-outline flex-1 sm:flex-none" @click="load">Batal</button>
          <button class="btn-primary flex-1 sm:flex-none" :disabled="busy"><Save class="size-4" /> Simpan Pengaturan</button>
        </div>
      </div>
    </form>

    <form v-else-if="tab === 'keamanan'" class="card max-w-xl space-y-5 p-5 sm:p-6" @submit.prevent="gantiPw">
      <div class="flex items-center gap-3"><KeyRound class="size-5 text-primary" /><h2 class="font-semibold">Ubah Kata Sandi</h2></div>
      <div><label class="label" for="pl">Kata Sandi Lama</label><input id="pl" v-model="pw.lama" type="password" autocomplete="current-password" required class="input"></div>
      <div><label class="label" for="pb">Kata Sandi Baru</label><input id="pb" v-model="pw.baru" type="password" autocomplete="new-password" minlength="8" required class="input"><p class="mt-1 text-xs text-muted">Minimal 8 karakter.</p></div>
      <div><label class="label" for="pu">Ulangi Kata Sandi Baru</label><input id="pu" v-model="pw.ulang" type="password" autocomplete="new-password" minlength="8" required class="input"></div>
      <div class="flex items-start gap-3 rounded-lg bg-slate-50 p-4 text-sm">
        <ShieldCheck class="mt-0.5 size-5 shrink-0 text-muted" />
        <p class="text-muted">Sesi login berlaku 8 jam. Autentikasi dua langkah (2FA) belum tersedia.</p>
      </div>
      <button class="btn-primary w-full sm:w-auto" :disabled="busy">Ubah Kata Sandi</button>
    </form>

    <div v-else class="card max-w-xl divide-y divide-line">
      <label v-for="[k, l, d] in [['aspirasi', 'Notifikasi Aspirasi', 'Saat warga mengirim aspirasi baru'], ['laporan', 'Notifikasi Laporan', 'Saat laporan dipublikasikan'], ['email', 'Email Notification', 'Kirim ringkasan ke email kedinasan']] as const" :key="k" class="flex items-center justify-between gap-4 p-5">
        <span><span class="block text-sm font-medium">{{ l }}</span><span class="text-xs text-muted">{{ d }}</span></span>
        <ToggleSwitch v-model="pref[k]" :label="l" />
      </label>
    </div>
  </div>
</template>
