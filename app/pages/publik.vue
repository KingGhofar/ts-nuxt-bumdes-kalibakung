<script setup lang="ts">
import { Landmark, FileText, Download, Store, Send, MapPin, Phone, Mail, User } from 'lucide-vue-next'
definePageMeta({ layout: 'blank' })
useHead({ title: 'Portal Transparansi · BUMDes Maju Jaya' })
const toast = useToast()
const { data } = await useFetch<any>('/api/public')
const b = computed(() => data.value?.bumdes)
const total = computed(() => (data.value?.laporan ?? []).reduce((a: any, l: any) => ({ in: a.in + l.totalPemasukan, out: a.out + l.totalPengeluaran }), { in: 0, out: 0 }))
const f = reactive({ nama: '', kategori: '', whatsapp: '', dusun: '', pesan: '' })
const busy = ref(false)

async function kirim() {
  busy.value = true
  try {
    await $fetch('/api/public/aspirasi', { method: 'POST', body: f })
    Object.assign(f, { nama: '', kategori: '', whatsapp: '', dusun: '', pesan: '' })
    toast.success('Terima kasih! Aspirasi Anda telah terkirim.')
  } catch (e) { toast.error(e) } finally { busy.value = false }
}
</script>

<template>
  <div class="bg-white">
    <header class="sticky top-0 z-20 border-b border-line bg-white/90 backdrop-blur">
      <div class="mx-auto flex max-w-6xl items-center gap-3 px-4 py-3">
        <img v-if="b?.logo" :src="fileUrl(b.logo)" alt="" class="size-9 rounded-lg object-cover">
        <span v-else class="grid size-9 place-items-center rounded-lg bg-primary text-white"><Landmark class="size-5" /></span>
        <span class="font-bold">{{ b?.nama ?? 'BUMDes' }}</span>
        <nav class="ml-auto hidden gap-6 text-sm font-medium text-muted md:flex">
          <a href="#profil" class="hover:text-primary">Profil</a><a href="#unit" class="hover:text-primary">Unit Usaha</a>
          <a href="#laporan" class="hover:text-primary">Laporan</a><a href="#aspirasi" class="hover:text-primary">Aspirasi</a>
        </nav>
        <NuxtLink to="/login" class="btn-primary ml-4 py-1.5 md:ml-6">Masuk Admin</NuxtLink>
      </div>
    </header>

    <section class="bg-sidebar px-4 py-20 text-center text-white">
      <p class="text-sm font-semibold uppercase tracking-widest text-blue-300">Portal Transparansi Publik</p>
      <h1 class="mx-auto mt-4 max-w-3xl text-3xl font-bold md:text-5xl">{{ b?.deskripsi || 'Menggerakkan Ekonomi Desa, Membangun Kesejahteraan Bersama' }}</h1>
      <p class="mt-4 text-slate-400">{{ b?.nama }} · Berdiri {{ b?.tahunBerdiri }}</p>
    </section>

    <main class="mx-auto max-w-6xl space-y-20 px-4 py-16">
      <section id="profil" class="grid gap-8 md:grid-cols-2">
        <div>
          <h2 class="text-2xl font-bold">Visi &amp; Misi</h2>
          <p class="mt-4 font-medium">{{ b?.visi }}</p>
          <p class="mt-4 whitespace-pre-line text-sm leading-relaxed text-muted">{{ b?.misi }}</p>
        </div>
        <div class="card space-y-3 p-6 text-sm">
          <p class="flex gap-2"><MapPin class="size-4 shrink-0 text-primary" /> {{ b?.alamat }}</p>
          <p class="flex gap-2"><Phone class="size-4 text-primary" /> {{ b?.telepon }}</p>
          <p class="flex gap-2"><Mail class="size-4 text-primary" /> {{ b?.email }}</p>
          <p class="border-t border-line pt-3 text-xs text-muted">{{ b?.dasarHukum }}</p>
        </div>
      </section>

      <section id="unit">
        <h2 class="text-2xl font-bold">Unit Usaha BUMDes</h2>
        <div class="mt-6 grid gap-6 md:grid-cols-3">
          <article v-for="u in data?.unit" :key="u.id" class="card overflow-hidden">
            <div class="relative h-40 bg-gradient-to-br from-blue-100 to-slate-200">
              <img v-if="u.foto" :src="fileUrl(u.foto)" alt="" class="size-full object-cover">
              <Store v-else class="absolute inset-0 m-auto size-10 text-slate-400" />
            </div>
            <div class="p-5">
              <p class="text-xs font-semibold uppercase tracking-wider text-primary">{{ u.kategori }}</p>
              <h3 class="mt-1 font-semibold">{{ u.nama }}</h3>
              <p class="mt-2 text-sm text-muted">{{ u.deskripsi }}</p>
              <p class="mt-3 flex items-center gap-1.5 text-xs text-muted"><User class="size-3.5" /> {{ u.penanggungJawab }}</p>
            </div>
          </article>
        </div>
      </section>

      <section id="laporan">
        <h2 class="text-2xl font-bold">Laporan Keuangan &amp; LPJ</h2>
        <p class="mt-1 text-sm text-muted">Hanya laporan yang telah dipublikasikan pengurus.</p>
        <div class="mt-6 grid gap-4 md:grid-cols-3">
          <StatCard label="Total Pendapatan" :value="rupiah(total.in)" tone="green" />
          <StatCard label="Total Beban Usaha" :value="rupiah(total.out)" tone="red" />
          <StatCard label="Laba Bersih" :value="rupiah(total.in - total.out)" />
        </div>
        <div class="card mt-6 overflow-x-auto">
          <table class="w-full min-w-[640px]">
            <thead class="border-b border-line bg-slate-50"><tr><th class="th">Periode</th><th class="th">Pemasukan</th><th class="th">Pengeluaran</th><th class="th">Saldo Bersih</th><th class="th">Dokumen</th></tr></thead>
            <tbody class="divide-y divide-line">
              <tr v-for="l in data?.laporan" :key="l.id">
                <td class="td font-medium">{{ periode(l.bulan, l.tahun) }}</td>
                <td class="td">{{ rupiah(l.totalPemasukan) }}</td>
                <td class="td">{{ rupiah(l.totalPengeluaran) }}</td>
                <td class="td font-semibold" :class="l.totalPemasukan >= l.totalPengeluaran ? 'text-green-600' : 'text-red-600'">{{ rupiah(l.totalPemasukan - l.totalPengeluaran) }}</td>
                <td class="td"><a v-if="l.fileLpj" :href="fileUrl(l.fileLpj)" target="_blank" class="inline-flex items-center gap-1.5 text-primary"><FileText class="size-4" /> LPJ <Download class="size-3.5" /></a><span v-else class="text-xs text-muted">—</span></td>
              </tr>
              <tr v-if="!data?.laporan.length"><td colspan="5" class="td py-10 text-center text-muted">Belum ada laporan dipublikasikan.</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <section id="aspirasi" class="grid gap-8 md:grid-cols-2">
        <div>
          <h2 class="text-2xl font-bold">Aspirasi &amp; Masukan Warga</h2>
          <p class="mt-3 text-muted">Punya kritik membangun, saran perluasan usaha, atau kendala fasilitas desa? Sampaikan secara langsung melalui form ini. Semua saran dicatat dan ditindaklanjuti secara berkala dalam musyawarah desa.</p>
        </div>
        <form class="card space-y-4 p-6" @submit.prevent="kirim">
          <div><label class="label" for="pn">Nama Lengkap *</label><input id="pn" v-model="f.nama" required maxlength="100" class="input" placeholder="Contoh: Budi Santoso"></div>
          <div class="grid gap-4 sm:grid-cols-2">
            <div><label class="label" for="pk">Kategori *</label><select id="pk" v-model="f.kategori" required class="input"><option value="" disabled>Pilih…</option><option v-for="k in KATEGORI_ASPIRASI" :key="k">{{ k }}</option></select></div>
            <div><label class="label" for="pd">Dusun</label><select id="pd" v-model="f.dusun" class="input"><option value="">—</option><option v-for="d in DUSUN" :key="d">{{ d }}</option></select></div>
          </div>
          <div><label class="label" for="pw">Nomor WhatsApp (opsional)</label><input id="pw" v-model="f.whatsapp" maxlength="30" class="input" placeholder="0812-xxxx-xxxx"></div>
          <div><label class="label" for="pp">Pesan Anda *</label><textarea id="pp" v-model="f.pesan" required minlength="5" maxlength="2000" rows="4" class="input" placeholder="Jelaskan masukan, pertanyaan, atau kendala yang dihadapi secara ringkas dan santun…" /></div>
          <button class="btn-primary w-full" :disabled="busy"><Send class="size-4" /> Kirim Aspirasi</button>
        </form>
      </section>
    </main>

    <footer class="bg-sidebar px-4 py-8 text-center text-sm text-slate-400">© {{ new Date().getFullYear() }} {{ b?.nama }} · Pemerintah Desa Maju Jaya</footer>
  </div>
</template>
