<script setup lang="ts">
import {
  Lock, FileText, MessageSquarePlus, ShieldCheck, CircleCheck, Sparkles, Handshake, ArrowUpRight, Briefcase, LineChart, Users,
  Droplets, Trees, Tractor, Recycle, Trophy, Store, ArrowRight, FileCheck2, Download, Archive, CheckCheck, Send, User, Tag, Phone,
  MapPin, Mail, Menu, X, UserRound, Target, Flag,
} from 'lucide-vue-next'
definePageMeta({ layout: 'blank' })
useHead({ title: 'Portal Transparansi Publik' })

const toast = useToast()
const { data } = await useFetch<any>('/api/public')
const b = computed(() => data.value?.bumdes)
const laporan = computed<any[]>(() => data.value?.laporan ?? [])
const nav = [['beranda', 'Beranda'], ['profil', 'Profil'], ['unit', 'Unit Usaha'], ['laporan', 'Laporan'], ['aspirasi', 'Aspirasi']] as const
const menu = ref(false)
const tahunIni = new Date().getFullYear()

// Pecah nama "BUMDes Desa Kalibakung" → aksen hijau di kata setelah "BUMDes".
const namaParts = computed(() => {
  const n = b.value?.nama ?? 'BUMDes'
  const m = n.match(/^(BUMDes)\s+(.*)$/i)
  return m ? [m[1], m[2]] : [n, '']
})
const kecamatan = computed(() => b.value?.alamat?.match(/Kec(?:amatan|\.)\s*([A-Za-z]+)/i)?.[1])

// Ringkasan dari laporan yang DIPUBLIKASIKAN saja.
const total = computed(() => laporan.value.reduce((a, l) => ({ in: a.in + l.totalPemasukan, out: a.out + l.totalPengeluaran }), { in: 0, out: 0 }))
const chart = computed(() => laporan.value.slice(0, 6).reverse())
const max = computed(() => Math.max(1, ...chart.value.flatMap(l => [l.totalPemasukan, l.totalPengeluaran])))
const denganLpj = computed(() => laporan.value.filter(l => l.fileLpj))
const lpjTerbaru = computed(() => denganLpj.value[0])
const juta = (n: number) => `Rp ${(n / 1e6).toLocaleString('id-ID', { maximumFractionDigits: 1 })} Jt`

// Ikon & warna unit ditebak dari kategori/nama.
function unitStyle(u: any) {
  const s = `${u.kategori} ${u.nama}`.toLowerCase()
  if (/air|pam|tirta/.test(s)) return { icon: Droplets, grad: 'from-blue-100 to-sky-50', fg: 'text-blue-500' }
  if (/sampah|daur/.test(s)) return { icon: Recycle, grad: 'from-teal-100 to-emerald-50', fg: 'text-teal-600' }
  if (/olahraga|lapangan|sport/.test(s)) return { icon: Trophy, grad: 'from-violet-100 to-indigo-50', fg: 'text-violet-500' }
  if (/wisata|kalimus/.test(s)) return { icon: Trees, grad: 'from-emerald-100 to-green-50', fg: 'text-emerald-600' }
  if (/tani|alsintan|pertanian/.test(s)) return { icon: Tractor, grad: 'from-amber-100 to-yellow-50', fg: 'text-amber-500' }
  return { icon: Store, grad: 'from-slate-100 to-slate-50', fg: 'text-slate-500' }
}
const jam = computed(() => (b.value?.jamOperasional ?? '').split('\n').map((l: string) => l.split('|').map(s => s.trim())).filter((r: string[]) => r[0]))
const misi = computed(() => (b.value?.misi ?? '').split('\n').map((s: string) => s.replace(/^\s*\d+[.)]\s*/, '').trim()).filter(Boolean))
const inisial = (n: string) => n.replace(/^(Bpk|Ibu|Pak|Sdr|Sdri)\.?\s+/i, '').split(/\s+/).map(s => s[0]).slice(0, 2).join('').toUpperCase()

const f = reactive({ nama: '', kategori: '', whatsapp: '', dusun: '', pesan: '', website: '' })
const busy = ref(false)
async function kirim() {
  busy.value = true
  try {
    await $fetch('/api/public/aspirasi', { method: 'POST', body: f })
    Object.assign(f, { nama: '', kategori: '', whatsapp: '', dusun: '', pesan: '' })
    toast.success('Terima kasih! Aspirasi Anda telah terkirim ke pengurus.')
  } catch (e) { toast.error(e) } finally { busy.value = false }
}
</script>

<template>
  <div class="bg-white font-display text-ink">
    <!-- NAVBAR -->
    <header class="sticky top-0 z-30 border-b border-slate-100 bg-white/90 backdrop-blur">
      <div class="mx-auto flex h-[72px] max-w-7xl items-center gap-4 px-4 sm:px-8">
        <a href="#beranda" class="flex min-w-0 items-center gap-3">
          <BrandMark tone="green" size="size-11" />
          <span class="min-w-0">
            <span class="block truncate text-lg font-bold leading-tight">{{ namaParts[0] }} <span class="text-brand">{{ namaParts[1] }}</span></span>
            <span class="block text-[10px] font-semibold uppercase tracking-[0.15em] text-muted">Transparansi &amp; Akuntabilitas</span>
          </span>
        </a>
        <nav class="mx-auto hidden rounded-full border border-slate-200 bg-slate-100/80 p-1 lg:flex" aria-label="Navigasi portal">
          <a v-for="[id, l] in nav" :key="id" :href="`#${id}`" class="rounded-full px-4 py-1.5 text-sm font-medium text-slate-600 transition hover:bg-white hover:text-brand-dark hover:shadow-sm">{{ l }}</a>
        </nav>
        <NuxtLink to="/login" class="btn ml-auto hidden rounded-full border border-slate-300 bg-white px-5 py-2.5 hover:bg-slate-50 lg:ml-0 lg:inline-flex"><Lock class="size-4" /> Login Pengurus</NuxtLink>
        <button class="icon-btn ml-auto lg:hidden" :aria-expanded="menu" aria-label="Menu" @click="menu = !menu"><component :is="menu ? X : Menu" class="size-6" /></button>
      </div>
      <div v-if="menu" class="border-t border-slate-100 bg-white px-4 pb-4 lg:hidden">
        <a v-for="[id, l] in nav" :key="id" :href="`#${id}`" class="block rounded-lg px-3 py-3 font-medium hover:bg-slate-50" @click="menu = false">{{ l }}</a>
        <NuxtLink to="/login" class="btn mt-2 w-full rounded-full border border-slate-300"><Lock class="size-4" /> Login Pengurus</NuxtLink>
      </div>
    </header>

    <main>
      <!-- HERO -->
      <section id="beranda" class="relative scroll-mt-20 overflow-hidden">
        <div class="pointer-events-none absolute -left-32 top-40 size-96 rounded-full bg-emerald-100/70 blur-3xl" />
        <div class="pointer-events-none absolute -right-20 top-0 size-96 rounded-full bg-blue-100/60 blur-3xl" />
        <div class="relative mx-auto grid max-w-7xl grid-cols-1 items-center gap-12 px-4 py-14 sm:px-8 lg:grid-cols-[1.4fr_1fr] lg:py-20">
          <div class="min-w-0">
            <span class="inline-flex flex-wrap items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-1.5 text-sm">
              <span class="size-2 rounded-full bg-brand" /><b class="text-brand-dark">Transparan &amp; Inovatif</b><span class="text-emerald-300">•</span><span class="text-brand">Portal Publik Resmi</span>
            </span>
            <h1 class="mt-6 break-words text-[2rem] font-extrabold leading-[1.05] tracking-tight sm:text-5xl lg:text-6xl">
              Menggerakkan Ekonomi Desa, <span class="bg-gradient-to-r from-brand to-teal-500 bg-clip-text text-transparent">Membangun Kesejahteraan</span> Bersama
            </h1>
            <p class="mt-6 max-w-2xl text-base leading-relaxed text-slate-600 sm:text-lg">
              {{ b?.deskripsi || 'Wadah keterbukaan informasi dan pertanggungjawaban unit usaha milik masyarakat. Bersama mengelola potensi desa yang mandiri, akuntabel, dan berkelanjutan untuk kemakmuran warga.' }}
            </p>
            <div class="mt-8 flex flex-col gap-3 sm:flex-row">
              <a href="#laporan" class="btn bg-brand px-6 py-4 text-base text-white shadow-lg shadow-emerald-600/30 hover:bg-brand-dark"><FileText class="size-5" /> Lihat Laporan Keuangan</a>
              <a href="#aspirasi" class="btn border border-slate-200 bg-white px-6 py-4 text-base shadow-sm hover:bg-slate-50"><MessageSquarePlus class="size-5" /> Sampaikan Aspirasi</a>
            </div>
            <div class="mt-8 flex flex-col gap-3 border-t border-slate-200 pt-6 text-sm text-slate-600 sm:flex-row sm:gap-8">
              <span class="flex items-center gap-2"><ShieldCheck class="size-5 shrink-0 text-brand" /> {{ b?.dasarHukum ? 'Berbadan hukum resmi' : 'Badan Usaha Milik Desa' }}</span>
              <span class="flex items-center gap-2"><CircleCheck class="size-5 shrink-0 text-blue-500" /> Laporan terbuka untuk warga</span>
            </div>
          </div>

          <div class="relative mx-auto w-full max-w-md">
            <div class="relative overflow-hidden rounded-3xl border-4 border-white bg-gradient-to-b from-emerald-500 to-emerald-700 p-6 shadow-2xl shadow-emerald-900/20">
              <div class="pointer-events-none absolute -right-10 -top-10 size-40 rounded-full bg-white/15 blur-2xl" />
              <svg class="pointer-events-none absolute inset-x-0 bottom-0 h-1/2 w-full text-emerald-900/30" viewBox="0 0 400 200" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 120 Q100 60 200 110 T400 90 V200 H0Z" /><path fill="currentColor" d="M0 160 Q120 110 240 150 T400 140 V200 H0Z" /></svg>
              <div class="relative flex items-start justify-between gap-2">
                <span class="inline-flex items-center gap-1.5 rounded-full border border-white/25 bg-white/15 px-3 py-1 text-xs font-semibold text-white"><Sparkles class="size-3.5" /> Desa Mandiri {{ tahunIni }}</span>
                <span v-if="kecamatan" class="rounded-full bg-black/25 px-3 py-1 text-xs font-semibold text-white">Kec. {{ kecamatan }}</span>
              </div>
              <div class="relative mt-16 rounded-2xl border border-white/20 bg-white/10 p-4 backdrop-blur-md">
                <span class="grid size-10 place-items-center rounded-xl bg-white text-brand"><Handshake class="size-5" /></span>
                <p class="mt-3 text-lg font-semibold text-white">Gotong Royong &amp; Mandiri</p>
                <p class="mt-1 text-sm text-white/85">Pengelolaan usaha desa secara profesional &amp; bermartabat demi masa depan generasi desa.</p>
              </div>
              <div class="relative mt-4 flex items-center gap-3 rounded-xl bg-white p-3 shadow-lg">
                <span class="grid size-10 shrink-0 place-items-center rounded-lg bg-emerald-50 text-sm font-bold text-brand">{{ laporan.length }}</span>
                <div class="min-w-0 flex-1"><p class="text-sm font-semibold">Laporan Terpublikasi</p><p class="truncate text-xs text-muted">Periode kas yang dapat diperiksa warga</p></div>
                <ArrowUpRight class="size-5 text-brand" />
              </div>
            </div>
          </div>
        </div>

        <!-- STATS -->
        <div class="relative mx-auto grid max-w-7xl grid-cols-1 gap-5 px-4 pb-16 sm:px-8 md:grid-cols-3">
          <div v-for="s in [
            { icon: Briefcase, tile: 'bg-emerald-50 text-brand', v: `${data?.unit.length ?? 0} Unit`, l: 'Unit Usaha Aktif', n: data?.unit.length ? 'Melayani kebutuhan warga desa' : 'Segera hadir' },
            { icon: LineChart, tile: 'bg-blue-50 text-blue-600', v: rupiah(total.in - total.out), l: 'Laba Bersih Terlapor', n: `Dari ${laporan.length} laporan terpublikasi` },
            { icon: Users, tile: 'bg-amber-50 text-amber-600', v: `${data?.stat.aspirasiSelesai ?? 0} / ${data?.stat.aspirasiTotal ?? 0}`, l: 'Aspirasi Ditindaklanjuti', n: 'Masukan warga yang tuntas ditangani' },
          ]" :key="s.l" class="flex items-center gap-5 rounded-2xl border border-slate-100 bg-white p-6 shadow-[0_4px_16px_rgba(15,23,42,.05)]">
            <span class="grid size-16 shrink-0 place-items-center rounded-2xl" :class="s.tile"><component :is="s.icon" class="size-7" /></span>
            <div class="min-w-0"><p class="truncate text-2xl font-extrabold">{{ s.v }}</p><p class="font-medium">{{ s.l }}</p><p class="truncate text-xs text-muted">{{ s.n }}</p></div>
          </div>
        </div>
      </section>

      <!-- PROFIL -->
      <section id="profil" class="scroll-mt-20 border-t border-slate-100 py-20">
        <div class="mx-auto max-w-7xl px-4 sm:px-8">
          <div class="mx-auto max-w-3xl text-center">
            <span class="rounded-full border border-emerald-200 bg-emerald-50 px-4 py-1 text-xs font-bold uppercase tracking-wider text-brand-dark">Profil Lembaga</span>
            <h2 class="mt-4 text-3xl font-extrabold tracking-tight sm:text-4xl">Mengenal {{ b?.nama }}</h2>
            <p class="mt-4 text-lg text-slate-600">{{ b?.alamat }}</p>
          </div>
          <div class="mt-12 grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div class="rounded-2xl bg-gradient-to-br from-emerald-600 to-emerald-800 p-8 text-white">
              <p class="mt-4 text-xs font-bold uppercase tracking-wider text-emerald-200">Visi</p>
              <p class="mt-2 text-xl font-semibold leading-relaxed">{{ b?.visi || 'Visi BUMDes akan segera diperbarui oleh pengurus.' }}</p>
            </div>
            <div class="rounded-2xl border border-emerald-100 bg-emerald-50/60 p-8">
              <p class="mt-4 text-xs font-bold uppercase tracking-wider text-brand-dark">Misi</p>
              <ol v-if="misi.length" class="mt-3 space-y-3">
                <li v-for="(m, i) in misi" :key="i" class="flex gap-3 text-slate-700"><span class="grid size-6 shrink-0 place-items-center rounded-full bg-emerald-100 text-xs font-bold text-brand-dark">{{ i + 1 }}</span>{{ m }}</li>
              </ol>
              <p v-else class="mt-2 text-slate-500">Misi BUMDes akan segera diperbarui oleh pengurus.</p>
            </div>
          </div>
          <div v-if="b?.pengurus?.length" class="mt-12">
            <h3 class="text-center text-xl font-bold">Struktur Pengurus</h3>
            <div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
              <div v-for="p in b.pengurus" :key="p.id" class="rounded-2xl border border-slate-100 bg-white p-6 text-center shadow-[0_4px_16px_rgba(15,23,42,.05)]">
                <img v-if="p.foto" :src="fileUrl(p.foto)" alt="" class="mx-auto size-20 rounded-full object-cover ring-4 ring-emerald-50">
                <span v-else class="mx-auto grid size-20 place-items-center rounded-full bg-emerald-50 text-brand ring-4 ring-emerald-50/50"><UserRound class="size-9" /></span>
                <p class="mt-4 font-bold">{{ p.nama }}</p>
                <p class="text-sm font-semibold text-brand">{{ p.jabatan }}</p>
                <p v-if="p.keterangan" class="mt-1 text-xs text-muted">{{ p.keterangan }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- UNIT USAHA -->
      <section id="unit" class="scroll-mt-20 border-y border-slate-100 bg-slate-50 py-20">
        <div class="mx-auto max-w-7xl px-4 sm:px-8">
          <div class="mx-auto max-w-3xl text-center">
            <span class="rounded-full border border-emerald-200 bg-emerald-50 px-4 py-1 text-xs font-bold uppercase tracking-wider text-brand-dark">Potensi &amp; Mandiri</span>
            <h2 class="mt-4 text-3xl font-extrabold tracking-tight sm:text-4xl">Layanan &amp; Unit Usaha Kami</h2>
            <p class="mt-4 text-lg text-slate-600">Solusi kebutuhan warga dan pengungkit ekonomi desa yang dikelola secara profesional, transparan, dan berorientasi pada kemajuan bersama.</p>
          </div>
          <div class="mt-12 grid grid-cols-1 gap-6 md:grid-cols-2" :class="data?.unit.length === 4 ? 'xl:grid-cols-4' : 'lg:grid-cols-3'">
            <article v-for="u in data?.unit" :key="u.id" class="flex min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-[0_4px_16px_rgba(15,23,42,.05)] transition hover:-translate-y-1 hover:shadow-lg">
              <div class="relative grid h-52 place-items-center bg-gradient-to-br" :class="unitStyle(u).grad">
                <img v-if="u.foto" :src="fileUrl(u.foto)" alt="" class="absolute inset-0 size-full object-cover">
                <span v-else class="grid size-20 place-items-center rounded-2xl bg-white shadow-lg"><component :is="unitStyle(u).icon" class="size-10" :class="unitStyle(u).fg" /></span>
                <span class="absolute right-4 top-4 inline-flex items-center gap-1.5 rounded-full bg-white px-3 py-1 text-xs font-semibold shadow-sm"><span class="size-2 rounded-full bg-brand" /> Beroperasi</span>
              </div>
              <div class="flex flex-1 flex-col p-6">
                <p class="text-xs font-semibold text-brand">{{ u.kategori }}</p>
                <h3 class="mt-1 text-xl font-bold">{{ u.nama }}</h3>
                <p class="mt-3 flex-1 text-sm leading-relaxed text-slate-600">{{ u.deskripsi }}</p>
                <div class="mt-5 flex items-center justify-between gap-3 border-t border-slate-100 pt-4 text-xs text-muted">
                  <span class="min-w-0 truncate">{{ u.metrikLabel ? `${u.metrikLabel}: ${u.metrikNilai}` : (u.penanggungJawab ? `PJ: ${u.penanggungJawab}` : u.kategori) }}</span>
                  <a href="#aspirasi" class="flex shrink-0 items-center gap-1 text-sm font-semibold text-brand hover:text-brand-dark">Beri Masukan <ArrowRight class="size-4" /></a>
                </div>
              </div>
            </article>
          </div>
          <p v-if="!data?.unit.length" class="mt-10 text-center text-slate-500">Unit usaha sedang disiapkan.</p>
        </div>
      </section>

      <!-- LAPORAN -->
      <section id="laporan" class="scroll-mt-20 py-20">
        <div class="mx-auto max-w-7xl px-4 sm:px-8">
          <div class="mx-auto max-w-3xl text-center">
            <span class="rounded-full border border-blue-200 bg-blue-50 px-4 py-1 text-xs font-bold uppercase tracking-wider text-blue-700">Akuntabilitas Terbuka</span>
            <h2 class="mt-4 text-3xl font-extrabold tracking-tight sm:text-4xl">Transparansi Laporan Keuangan</h2>
            <p class="mt-4 text-lg text-slate-600">Bentuk komitmen kami terhadap keterbukaan publik. Setiap rupiah dana masyarakat dilaporkan secara jujur, berkala, dan dapat diawasi bersama.</p>
          </div>

          <div class="mt-12 grid grid-cols-1 gap-6 rounded-3xl border border-slate-200 bg-slate-50 p-4 shadow-sm sm:p-8 lg:grid-cols-3">
            <div class="min-w-0 rounded-2xl border border-slate-200 bg-white p-5 sm:p-6 lg:col-span-2">
              <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <p class="flex flex-wrap items-center gap-2 text-lg font-bold">Pendapatan vs Pengeluaran <span class="rounded-full bg-emerald-100 px-2.5 py-0.5 text-xs font-semibold text-brand-dark">Terpublikasi</span></p>
                  <p class="text-sm text-muted">Realisasi kas operasional per bulan (dalam juta rupiah)</p>
                </div>
                <div v-if="chart.length" class="flex gap-4 text-xs text-slate-600">
                  <span class="flex items-center gap-1.5"><span class="size-2.5 rounded-sm bg-emerald-600" /> Pendapatan</span>
                  <span class="flex items-center gap-1.5"><span class="size-2.5 rounded-sm bg-blue-500" /> Pengeluaran</span>
                </div>
              </div>
              <div v-if="chart.length" class="mt-6">
                <div class="flex h-48 items-end gap-1.5 border-b border-slate-200 sm:h-56 sm:gap-3">
                  <div v-for="l in chart" :key="l.id" class="group relative flex h-full flex-1 items-end justify-center gap-1.5">
                    <span class="pointer-events-none absolute left-1/2 top-0 z-10 hidden -translate-x-1/2 whitespace-nowrap rounded bg-slate-800 px-2 py-1 text-[11px] text-white group-hover:block">{{ juta(l.totalPemasukan) }} / {{ juta(l.totalPengeluaran) }}</span>
                    <div class="w-1/3 max-w-6 rounded-t-md bg-emerald-600" :style="{ height: `${(l.totalPemasukan / max) * 90}%` }" />
                    <div class="w-1/3 max-w-6 rounded-t-md bg-blue-500" :style="{ height: `${(l.totalPengeluaran / max) * 90}%` }" />
                  </div>
                </div>
                <div class="flex gap-1.5 pt-2 sm:gap-3">
                  <span v-for="l in chart" :key="l.id" class="flex-1 text-center text-xs text-muted">{{ BULAN[l.bulan - 1].slice(0, 3) }}</span>
                </div>
              </div>
              <div v-else class="mt-6 grid place-items-center rounded-xl border border-dashed border-slate-200 py-14 text-center"><FileText class="size-8 text-slate-300" /><p class="mt-2 text-sm text-muted">Belum ada laporan yang dipublikasikan pengurus.</p></div>
              <div class="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-3">
                <div class="rounded-xl border border-slate-200 bg-slate-50 p-4"><p class="text-xs text-slate-600">Total Pendapatan</p><p class="mt-1 text-lg font-bold text-brand-dark">{{ rupiah(total.in) }}</p></div>
                <div class="rounded-xl border border-slate-200 bg-slate-50 p-4"><p class="text-xs text-slate-600">Total Beban Usaha</p><p class="mt-1 text-lg font-bold text-blue-700">{{ rupiah(total.out) }}</p></div>
                <div class="rounded-xl border border-emerald-200 bg-emerald-50 p-4"><p class="text-xs text-brand-dark">Laba Bersih</p><p class="mt-1 text-lg font-bold text-emerald-900">{{ total.in - total.out > 0 ? '+' : '' }}{{ rupiah(total.in - total.out) }}</p></div>
              </div>
            </div>

            <div class="flex min-w-0 flex-col gap-6">
              <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-800 to-emerald-950 p-6 text-white shadow-lg">
                <div class="pointer-events-none absolute -bottom-10 -right-10 size-40 rounded-full bg-emerald-400/20 blur-2xl" />
                <div class="relative flex items-center gap-3">
                  <span class="grid size-12 place-items-center rounded-xl border border-white/20 bg-white/15"><FileCheck2 class="size-6 text-emerald-200" /></span>
                  <span class="text-xs font-bold uppercase tracking-wider text-emerald-300">Laporan Resmi</span>
                </div>
                <p class="relative mt-5 text-lg font-bold">{{ lpjTerbaru ? `LPJ ${periode(lpjTerbaru.bulan, lpjTerbaru.tahun)}` : 'LPJ Terbaru' }}</p>
                <p class="relative mt-2 text-sm text-white/80">Dokumen Laporan Pertanggungjawaban (LPJ) memuat rincian pendapatan, beban usaha, dan saldo kas BUMDes.</p>
                <a v-if="lpjTerbaru" :href="fileUrl(lpjTerbaru.fileLpj)" target="_blank" class="relative mt-5 flex w-full items-center justify-center gap-2 rounded-xl bg-white py-3 font-bold text-emerald-900 hover:bg-emerald-50"><Download class="size-5" /> Unduh LPJ Terbaru</a>
                <p v-else class="relative mt-5 text-sm italic text-emerald-200/80">Dokumen LPJ akan tersedia setelah dipublikasikan pengurus.</p>
              </div>

              <div class="rounded-2xl border border-slate-200 bg-white p-5">
                <div class="flex items-center justify-between"><p class="text-xs font-bold uppercase tracking-wider text-slate-700">Arsip Laporan</p><Archive class="size-4 text-slate-400" /></div>
                <ul class="mt-3 max-h-72 divide-y divide-slate-100 overflow-y-auto">
                  <li v-for="l in laporan" :key="l.id" class="flex items-center gap-3 py-3">
                    <FileText class="size-5 shrink-0 text-red-500" />
                    <div class="min-w-0 flex-1">
                      <p class="truncate text-sm font-medium">Rekap Kas {{ periode(l.bulan, l.tahun) }}</p>
                      <p class="text-xs text-slate-400">Saldo {{ rupiah(l.totalPemasukan - l.totalPengeluaran) }}</p>
                    </div>
                    <a v-if="l.fileLpj" :href="fileUrl(l.fileLpj)" target="_blank" class="icon-btn size-8" :aria-label="`Unduh LPJ ${periode(l.bulan, l.tahun)}`"><Download class="size-4" /></a>
                  </li>
                  <li v-if="!laporan.length" class="py-6 text-center text-sm text-muted">Belum ada arsip.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ASPIRASI -->
      <section id="aspirasi" class="scroll-mt-20 bg-[#F0FAF5] py-20">
        <div class="mx-auto grid max-w-7xl grid-cols-1 gap-12 px-4 sm:px-8 lg:grid-cols-[1fr_1.4fr]">
          <div class="min-w-0">
            <span class="rounded-full border border-emerald-200 bg-emerald-100 px-4 py-1 text-xs font-bold uppercase tracking-wider text-brand-dark">Suara Warga Desa</span>
            <h2 class="mt-4 text-3xl font-extrabold tracking-tight sm:text-4xl">Aspirasi &amp; Masukan Warga</h2>
            <p class="mt-4 text-lg leading-relaxed text-slate-600">Punya kritik membangun, saran perluasan usaha, atau kendala fasilitas desa? Sampaikan langsung melalui form ini. Semua saran dicatat dan ditindaklanjuti secara berkala.</p>
            <template v-if="data?.aspirasi.length">
              <p class="mt-10 flex items-center gap-2 text-sm font-bold uppercase tracking-wider"><CheckCheck class="size-4 text-brand" /> Aspirasi Terbaru <span class="ml-auto text-xs font-semibold normal-case tracking-normal text-slate-400">{{ data.aspirasi.length }} pesan</span></p>
              <div class="mt-4 max-h-[19rem] space-y-4 overflow-y-auto overscroll-contain pr-2 [scrollbar-width:thin]" tabindex="0" aria-label="Daftar aspirasi terbaru">
                <div v-for="a in data.aspirasi" :key="a.id" class="rounded-2xl border border-emerald-100 bg-white p-5 shadow-sm">
                  <div class="flex items-center gap-3">
                    <span class="grid size-9 shrink-0 place-items-center rounded-full border border-slate-200 bg-slate-100 text-xs font-bold">{{ inisial(a.nama) }}</span>
                    <div class="min-w-0 flex-1"><p class="truncate text-sm font-semibold">{{ a.nama }}</p><p class="truncate text-[11px] text-slate-400">{{ [a.dusun, a.kategori].filter(Boolean).join(' • ') }}</p></div>
                    <StatusBadge :status="a.status" />
                  </div>
                  <p class="mt-3 break-words rounded-xl border border-slate-100 bg-slate-50 px-3 py-2.5 text-sm italic text-slate-700">“{{ a.pesan }}”</p>
                </div>
              </div>
            </template>
          </div>

          <form class="min-w-0 self-start rounded-3xl border border-emerald-100 bg-white p-5 shadow-[0_10px_30px_rgba(15,23,42,.05)] sm:p-10" @submit.prevent="kirim">
            <div class="flex items-center gap-4 border-b border-slate-100 pb-6">
              <span class="grid size-12 shrink-0 place-items-center rounded-xl bg-brand text-white shadow-md shadow-emerald-600/30"><Send class="size-5" /></span>
              <div><p class="text-xl font-bold">Formulir Aspirasi Publik</p><p class="text-sm text-muted">Kritik &amp; masukan langsung masuk ke dashboard pengurus.</p></div>
            </div>
            <div class="mt-6 space-y-5">
              <div>
                <label for="pn" class="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-800">Nama Lengkap <span class="text-red-500">*</span></label>
                <div class="relative"><User class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-400" /><input id="pn" v-model="f.nama" required maxlength="100" class="input py-3 pl-10" placeholder="Contoh: Budi Santoso"></div>
              </div>
              <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
                <div>
                  <label for="pk" class="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-800">Kategori <span class="text-red-500">*</span></label>
                  <div class="relative"><Tag class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
                    <select id="pk" v-model="f.kategori" required class="input py-3 pl-10"><option value="" disabled>Pilih kategori…</option><option v-for="k in KATEGORI_ASPIRASI" :key="k">{{ k }}</option></select></div>
                </div>
                <div>
                  <label for="pw" class="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-800">Nomor WhatsApp <span class="font-semibold normal-case text-slate-400">(opsional)</span></label>
                  <div class="relative"><Phone class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-400" /><input id="pw" v-model="f.whatsapp" type="tel" maxlength="30" class="input py-3 pl-10" placeholder="0812-xxxx-xxxx"></div>
                </div>
              </div>
              <div>
                <label for="pd" class="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-800">Dusun / RT-RW <span class="font-semibold normal-case text-slate-400">(opsional)</span></label>
                <div class="relative"><MapPin class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-400" /><input id="pd" v-model="f.dusun" maxlength="100" class="input py-3 pl-10" placeholder="Contoh: RT 01 / RW 03"></div>
              </div>
              <div>
                <label for="pp" class="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-800">Pesan Anda <span class="text-red-500">*</span></label>
                <textarea id="pp" v-model="f.pesan" required minlength="5" maxlength="2000" rows="4" class="input p-3.5" placeholder="Jelaskan masukan, pertanyaan, atau kendala yang dihadapi secara ringkas dan santun…" />
              </div>
              <!-- Honeypot anti-bot: disembunyikan dari manusia -->
              <input v-model="f.website" type="text" name="website" tabindex="-1" autocomplete="off" class="absolute -left-[9999px] size-px opacity-0" aria-hidden="true">
              <button class="btn w-full rounded-full bg-brand py-4 text-base font-bold text-white shadow-lg shadow-emerald-600/25 hover:bg-brand-dark" :disabled="busy">{{ busy ? 'Mengirim…' : 'Kirim Aspirasi Sekarang' }} </button>
            </div>
          </form>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
    <footer class="bg-[#111827] pt-16 text-slate-400">
      <div class="mx-auto grid max-w-7xl grid-cols-1 gap-10 px-4 sm:px-8 md:grid-cols-2 lg:grid-cols-[5fr_3fr_4fr]">
        <div class="min-w-0">
          <div class="flex items-center gap-3"><BrandMark tone="green" /><p class="text-xl font-bold text-white">{{ b?.nama }}</p></div>
          <p class="mt-6 max-w-sm leading-relaxed">Lembaga usaha ekonomi desa yang berdedikasi menciptakan kemandirian warga, keterbukaan pengelolaan aset, dan layanan desa berintegritas.</p>
          <ul class="mt-7 space-y-3 text-sm text-slate-300">
            <li v-if="b?.alamat" class="flex gap-3"><MapPin class="mt-0.5 size-4 shrink-0 text-emerald-400" /> {{ b.alamat }}</li>
            <li v-if="b?.telepon" class="flex gap-3"><Phone class="mt-0.5 size-4 shrink-0 text-emerald-400" /> {{ b.telepon }}</li>
            <li v-if="b?.email" class="flex gap-3"><Mail class="mt-0.5 size-4 shrink-0 text-emerald-400" /> <span class="break-all">{{ b.email }}</span></li>
          </ul>
        </div>
        <div>
          <p class="text-sm font-bold uppercase tracking-wider text-white">Tautan Cepat</p>
          <ul class="mt-5 space-y-3">
            <li v-for="[id, l] in [['beranda', 'Beranda Utama'], ['profil', 'Profil & Struktur Pengurus'], ['unit', 'Unit Usaha BUMDes'], ['laporan', 'Laporan Keuangan & LPJ'], ['aspirasi', 'Formulir Aspirasi Warga']]" :key="id"><a :href="`#${id}`" class="hover:text-white">{{ l }}</a></li>
          </ul>
        </div>
        <div>
          <p class="text-sm font-bold uppercase tracking-wider text-white">Jam Operasional Kantor</p>
          <p class="mt-4 text-sm">Silakan berkunjung langsung ke kantor BUMDes pada jam kerja berikut:</p>
          <div class="mt-4 divide-y divide-slate-700 rounded-xl border border-slate-700 bg-slate-800/60 px-4">
            <div v-for="(r, i) in jam" :key="i" class="flex items-center justify-between gap-3 py-3 text-sm">
              <span class="text-slate-300">{{ r[0] }}</span>
              <span class="text-right font-semibold" :class="/tutup/i.test(r[1] ?? '') ? 'text-red-400' : 'text-emerald-400'">{{ r[1] }}</span>
            </div>
            <p v-if="!jam.length" class="py-3 text-sm">Hubungi kantor untuk informasi jam layanan.</p>
          </div>
        </div>
      </div>
      <div class="mx-auto mt-12 flex max-w-7xl flex-col gap-2 border-t border-slate-800 px-4 py-8 text-sm text-slate-500 sm:flex-row sm:justify-between sm:px-8">
        <p>© {{ tahunIni }} {{ b?.nama }}. Hak Cipta Dilindungi Undang-Undang.</p>
        <NuxtLink to="/login" class="hover:text-white">Login Pengurus</NuxtLink>
      </div>
    </footer>
  </div>
</template>
