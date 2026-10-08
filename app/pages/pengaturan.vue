<script setup lang="ts">
import { BadgeCheck, KeyRound, ShieldCheck } from 'lucide-vue-next'
useHead({ title: 'Pengaturan · BUMDes Maju Jaya' })
const toast = useToast()
const { fetchMe } = useAuth()
const tab = ref<'profil' | 'keamanan' | 'notifikasi'>('profil')
const { data: akun } = await useFetch<any>('/api/akun')
const f = reactive({ nama: '', email: '', jabatan: '', telepon: '', unitKerja: '', avatar: null as string | null })
if (akun.value) Object.assign(f, Object.fromEntries(Object.keys(f).map(k => [k, akun.value[k] ?? (k === 'avatar' ? null : '')])))
const pw = reactive({ lama: '', baru: '', ulang: '' })
// ponytail: preferensi notifikasi disimpan di cookie browser saja. Pindah ke tabel bila perlu kirim email/WA sungguhan.
const pref = useCookie('notif-pref', { default: () => ({ aspirasi: true, laporan: true, email: false }) })
const busy = ref(false)

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
const tabs = [['profil', 'Profil Akun'], ['keamanan', 'Keamanan & Autentikasi'], ['notifikasi', 'Preferensi Notifikasi']] as const
</script>

<template>
  <div>
    <PageHeader title="Pengaturan Sistem" subtitle="Kelola akun, keamanan, dan preferensi notifikasi." :crumbs="[{ label: 'Pengaturan' }]">
      <span class="inline-flex items-center gap-1.5 rounded-full bg-green-50 px-3 py-1.5 text-xs font-semibold text-green-700"><BadgeCheck class="size-4" /> Status Akun: Terverifikasi</span>
    </PageHeader>

    <div class="mb-6 flex gap-1 overflow-x-auto border-b border-line" role="tablist">
      <button
        v-for="[k, l] in tabs" :key="k" role="tab" :aria-selected="tab === k"
        class="whitespace-nowrap border-b-2 px-4 py-2.5 text-sm font-medium"
        :class="tab === k ? 'border-primary text-primary' : 'border-transparent text-muted hover:text-ink'" @click="tab = k"
      >{{ l }}</button>
    </div>

    <form v-if="tab === 'profil'" class="card space-y-6 p-6" @submit.prevent="simpanProfil">
      <div>
        <label class="label">Foto Profil Administrator</label>
        <FileDrop v-model="f.avatar" kind="image" accept=".png,.jpg,.jpeg,.webp" hint="PNG/JPG, maksimal 2MB." />
      </div>
      <div>
        <h3 class="font-semibold">Data Diri &amp; Penugasan</h3>
        <p class="text-xs text-muted">Data ini digunakan untuk verifikasi pengesahan laporan dan audit keuangan.</p>
      </div>
      <div class="grid gap-5 md:grid-cols-2">
        <div><label class="label" for="nm">Nama Lengkap *</label><input id="nm" v-model="f.nama" required class="input"></div>
        <div><label class="label" for="em">Email Kedinasan *</label><input id="em" v-model="f.email" type="email" required class="input"></div>
        <div><label class="label" for="jb">Jabatan / Posisi</label><input id="jb" v-model="f.jabatan" class="input"></div>
        <div><label class="label" for="tl">Nomor Telepon / WhatsApp</label><input id="tl" v-model="f.telepon" class="input"></div>
        <div><label class="label" for="nik">NIK / Identitas Pegawai Desa</label><input id="nik" :value="akun?.nik" readonly class="input bg-slate-50 text-muted"></div>
        <div><label class="label" for="uk">Unit Kerja Penugasan</label><input id="uk" v-model="f.unitKerja" class="input"></div>
      </div>
      <div class="flex justify-end border-t border-line pt-5"><button class="btn-primary" :disabled="busy">Simpan Perubahan</button></div>
    </form>

    <form v-else-if="tab === 'keamanan'" class="card max-w-xl space-y-5 p-6" @submit.prevent="gantiPw">
      <div class="flex items-center gap-3"><KeyRound class="size-5 text-primary" /><h3 class="font-semibold">Ubah Password</h3></div>
      <div><label class="label" for="pl">Password Lama</label><input id="pl" v-model="pw.lama" type="password" autocomplete="current-password" required class="input"></div>
      <div><label class="label" for="pb">Password Baru</label><input id="pb" v-model="pw.baru" type="password" autocomplete="new-password" minlength="8" required class="input"></div>
      <div><label class="label" for="pu">Ulangi Password Baru</label><input id="pu" v-model="pw.ulang" type="password" autocomplete="new-password" minlength="8" required class="input"></div>
      <div class="flex items-start gap-3 rounded-lg bg-slate-50 p-4 text-sm">
        <ShieldCheck class="mt-0.5 size-5 text-muted" />
        <p class="text-muted">Sesi login berlaku 8 jam. Two-factor authentication belum tersedia.</p>
      </div>
      <button class="btn-primary" :disabled="busy">Ubah Password</button>
    </form>

    <div v-else class="card max-w-xl divide-y divide-line">
      <label v-for="[k, l, d] in [['aspirasi', 'Notifikasi Aspirasi', 'Saat warga mengirim aspirasi baru'], ['laporan', 'Notifikasi Laporan', 'Saat laporan dipublikasikan'], ['email', 'Email Notification', 'Kirim ringkasan ke email kedinasan']] as const" :key="k" class="flex items-center justify-between p-5">
        <span><span class="block text-sm font-medium">{{ l }}</span><span class="text-xs text-muted">{{ d }}</span></span>
        <ToggleSwitch v-model="pref[k]" :label="l" />
      </label>
    </div>
  </div>
</template>
