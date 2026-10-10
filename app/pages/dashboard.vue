<script setup lang="ts">
import { Wallet, TrendingUp, TrendingDown, MessageSquareText, Store, Eye, Download, AlertCircle, History, ShieldCheck, CalendarDays } from 'lucide-vue-next'
useHead({ title: 'Dashboard' })

const { user } = useAuth()
const brand = useBrand()
const range = ref<'6' | 'tahun'>('6')
const { data } = await useFetch<any>('/api/dashboard', { query: { range } })
const max = computed(() => Math.max(1, ...(data.value?.chart ?? []).flatMap((c: any) => [c.pemasukan, c.pengeluaran])))
const juta = (n: number) => `Rp ${(n / 1e6).toLocaleString('id-ID', { maximumFractionDigits: 1 })} Jt`
const now = new Date().toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
const dot: Record<string, string> = { aspirasi: 'bg-blue-600', laporan: 'bg-emerald-500', unit: 'bg-amber-500' }
</script>

<template>
  <div v-if="data">
    <div class="mb-5 flex flex-wrap items-center justify-between gap-2 text-sm">
      <p><span class="font-semibold text-primary">Dashboard</span> <span class="text-slate-400">/</span> Beranda Utama</p>
      <p class="flex items-center gap-1.5 text-muted"><CalendarDays class="size-4 text-primary" /> {{ now }}</p>
    </div>

    <!-- Hero -->
    <section class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-600 via-blue-600 to-emerald-700 p-6 text-white sm:p-8">
      <div class="pointer-events-none absolute -right-16 -top-16 size-64 rounded-full bg-white/10 blur-2xl" />
      <span class="inline-flex items-center gap-2 rounded-full border border-white/30 bg-white/15 px-3 py-1 text-xs font-semibold">
        <span class="size-2 rounded-full bg-green-400" /> Ringkasan Operasional Terkini
      </span>
      <h1 class="mt-4 text-2xl font-bold sm:text-3xl">Selamat Datang, {{ user?.nama }}!</h1>
      <p class="mt-2 max-w-2xl text-sm text-white/90">
        Berikut ringkasan performa {{ brand.nama }}. Laporan yang dipublikasikan langsung tampil di Portal Transparansi Publik desa.
      </p>
      <div class="mt-6 flex flex-col gap-2 sm:flex-row">
        <NuxtLink to="/publik" target="_blank" class="btn border border-white/30 bg-white/15 text-white hover:bg-white/25"><Eye class="size-4" /> Lihat Transparansi Publik</NuxtLink>
        <a href="/api/laporan/export" class="btn bg-white text-primary-hover hover:bg-blue-50"><Download class="size-4" /> Unduh Rekap Laporan</a>
      </div>
    </section>

    <!-- Stats -->
    <div class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <StatCard label="Total Saldo Kas" :value="rupiah(data.saldoKas)" :icon="Wallet">
        <span class="truncate">Akumulasi seluruh periode</span>
      </StatCard>
      <StatCard label="Laba Bulan Ini" :value="(data.labaBulanIni > 0 ? '+' : '') + rupiah(data.labaBulanIni)" :icon="TrendingUp" :tone="data.labaBulanIni >= 0 ? 'green' : 'red'">
        <span v-if="data.labaGrowth !== null" class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 font-semibold" :class="data.labaGrowth >= 0 ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-600'">
          <component :is="data.labaGrowth >= 0 ? TrendingUp : TrendingDown" class="size-3" /> {{ persen(data.labaGrowth, 0) }}
        </span>
        <span class="truncate">{{ data.periodeTerakhir ? `per ${data.periodeTerakhir}` : 'Belum ada laporan' }}</span>
      </StatCard>
      <StatCard label="Aspirasi Menunggu" :value="`${data.aspirasiMenunggu} Pesan`" :icon="MessageSquareText" tone="amber">
        <AlertCircle class="size-3.5 shrink-0 text-amber-600" /><span class="truncate text-amber-700">Perlu tinjauan &amp; tanggapan</span>
      </StatCard>
      <StatCard label="Unit Usaha Aktif" :value="`${data.unitAktif} Unit`" :icon="Store">
        <span class="truncate" :title="data.unitNama.join(', ')">{{ data.unitNama.join(', ') || 'Belum ada unit' }}</span>
      </StatCard>
    </div>

    <div class="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-3">
      <!-- Chart -->
      <section class="card min-w-0 p-5 sm:p-6 xl:col-span-2">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h2 class="font-semibold">Arus Kas &amp; Pendapatan</h2>
            <p class="text-xs text-muted">Perbandingan kas masuk vs belanja operasional</p>
          </div>
          <div class="inline-flex self-start rounded-lg border border-blue-100 bg-blue-50 p-1 text-xs font-semibold">
            <button v-for="[k, l] in [['6', '6 Bulan'], ['tahun', `Tahun ${new Date().getFullYear()}`]] as const" :key="k"
              class="rounded-md px-3 py-1.5 transition" :class="range === k ? 'bg-white text-primary shadow-sm' : 'text-slate-600'" @click="range = k">{{ l }}</button>
          </div>
        </div>
        <div class="mt-4 flex flex-wrap gap-4 text-xs text-slate-600">
          <span class="flex items-center gap-1.5"><span class="size-2.5 rounded-sm bg-emerald-500" /> Pemasukan</span>
          <span class="flex items-center gap-1.5"><span class="size-2.5 rounded-sm bg-blue-500" /> Pengeluaran</span>
        </div>

        <div v-if="data.chart.length" class="mt-4">
          <div class="flex h-48 items-end gap-1 border-b border-line sm:h-60 sm:gap-2">
            <div v-for="(c, i) in data.chart" :key="i" class="group relative flex h-full flex-1 flex-col justify-end rounded-t-md" :class="{ 'bg-slate-50': i === data.chart.length - 1 }">
              <span class="pointer-events-none absolute -top-1 left-1/2 z-10 hidden -translate-x-1/2 -translate-y-full whitespace-nowrap rounded bg-slate-800 px-2 py-1 text-[11px] text-white group-hover:block">
                {{ juta(c.pemasukan) }} / {{ juta(c.pengeluaran) }}
              </span>
              <div class="flex h-[92%] items-end justify-center gap-1">
                <div class="w-[38%] max-w-7 rounded-t bg-emerald-500" :style="{ height: `${(c.pemasukan / max) * 100}%` }" />
                <div class="w-[38%] max-w-7 rounded-t bg-blue-500" :style="{ height: `${(c.pengeluaran / max) * 100}%` }" />
              </div>
            </div>
          </div>
          <div class="flex gap-1 pt-2 sm:gap-2">
            <span v-for="(c, i) in data.chart" :key="i" class="flex-1 text-center text-[11px] sm:text-xs" :class="i === data.chart.length - 1 ? 'font-bold text-primary' : 'text-muted'">{{ c.label }}</span>
          </div>
        </div>
        <p v-else class="py-16 text-center text-sm text-muted">Belum ada data laporan. <NuxtLink to="/laporan-keuangan/tambah" class="font-semibold text-primary">Tambah laporan →</NuxtLink></p>

        <div class="mt-6 grid gap-4 border-t border-line pt-5 sm:grid-cols-3">
          <div>
            <p class="text-xs text-muted">Rata-rata Pemasukan Bulanan</p>
            <p class="font-bold">{{ rupiah(data.rataPemasukan) }}</p>
          </div>
          <div>
            <p class="text-xs text-muted">Rasio Efisiensi Belanja</p>
            <p class="font-bold" :class="data.rasioBelanja < 65 ? 'text-primary' : 'text-red-600'">{{ persen(data.rasioBelanja) }}</p>
            <p class="text-[11px] text-muted">Batas aman &lt; 65%</p>
          </div>
          <div>
            <p class="text-xs text-muted">Surplus Periode Grafik</p>
            <p class="font-bold" :class="data.surplus >= 0 ? 'text-emerald-700' : 'text-red-600'">{{ rupiah(data.surplus) }}</p>
          </div>
        </div>
      </section>

      <!-- Activity -->
      <section class="card flex flex-col p-5 sm:p-6">
        <div class="flex items-center justify-between">
          <h2 class="flex items-center gap-2 font-semibold"><History class="size-4 text-primary" /> Aktivitas Terbaru</h2>
          <NuxtLink to="/notifikasi" class="text-xs font-semibold text-primary">Lihat Semua</NuxtLink>
        </div>
        <ol v-if="data.aktivitas.length" class="mt-5 flex-1 space-y-5 border-l border-line pl-5">
          <li v-for="a in data.aktivitas" :key="a.id" class="relative">
            <span class="absolute -left-[26.5px] top-1 size-3 rounded-full ring-4 ring-white" :class="dot[a.tipe] ?? 'bg-slate-500'" />
            <p class="text-sm font-semibold">{{ a.judul }}</p>
            <p class="line-clamp-2 text-xs text-muted">{{ a.pesan }}</p>
            <p class="mt-1 text-[11px] text-slate-400">{{ waktuLalu(a.createdAt) }}</p>
          </li>
        </ol>
        <p v-else class="flex-1 py-10 text-center text-sm text-muted">Belum ada aktivitas.</p>
        <NuxtLink to="/notifikasi" class="btn-outline mt-6 w-full"><ShieldCheck class="size-4" /> Buka Riwayat Aktivitas</NuxtLink>
      </section>
    </div>
  </div>
</template>
