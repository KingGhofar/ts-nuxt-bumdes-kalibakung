<script setup lang="ts">
import { Wallet, TrendingUp, MessageSquareText, Store, Plus, FileBarChart, Bell } from 'lucide-vue-next'
useHead({ title: 'Dashboard · BUMDes Maju Jaya' })

const { user } = useAuth()
const { data } = await useFetch<any>('/api/dashboard')
const max = computed(() => Math.max(1, ...(data.value?.chart ?? []).flatMap((c: any) => [c.pemasukan, c.pengeluaran])))
</script>

<template>
  <div v-if="data">
    <div class="mb-6 rounded-xl bg-gradient-to-r from-primary to-blue-500 p-6 text-white">
      <span class="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold">Operasional · Tahun Anggaran {{ new Date().getFullYear() }}</span>
      <h1 class="mt-3 text-2xl font-bold">Selamat Datang, {{ user?.nama }}</h1>
      <p class="mt-1 text-sm text-blue-100">Data rekap terakhir: {{ data.periodeTerakhir ?? 'belum ada laporan' }}</p>
      <div class="mt-4 flex flex-wrap gap-2">
        <NuxtLink to="/laporan-keuangan/tambah" class="btn bg-white text-primary hover:bg-blue-50"><Plus class="size-4" /> Tambah Laporan</NuxtLink>
        <NuxtLink to="/unit-usaha/tambah" class="btn bg-white/15 text-white hover:bg-white/25"><Store class="size-4" /> Tambah Unit</NuxtLink>
      </div>
    </div>

    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <StatCard label="Total Saldo Kas" :value="rupiah(data.saldoKas)" :icon="Wallet" />
      <StatCard label="Laba Bulan Ini" :value="(data.labaBulanIni >= 0 ? '+ ' : '') + rupiah(data.labaBulanIni)" :icon="TrendingUp" tone="green" />
      <StatCard label="Aspirasi Menunggu" :value="`${data.aspirasiMenunggu} Pesan`" :icon="MessageSquareText" tone="amber" />
      <StatCard label="Unit Usaha Aktif" :value="`${data.unitAktif} Unit`" :icon="Store" />
    </div>

    <div class="mt-6 grid gap-6 xl:grid-cols-3">
      <section class="card p-6 xl:col-span-2">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 class="font-semibold">Arus Kas</h2>
            <p class="text-xs text-muted">6 periode laporan terakhir</p>
          </div>
          <div class="flex gap-4 text-xs">
            <span class="flex items-center gap-1.5"><span class="size-2.5 rounded-sm bg-primary" /> Pemasukan</span>
            <span class="flex items-center gap-1.5"><span class="size-2.5 rounded-sm bg-red-400" /> Pengeluaran</span>
          </div>
        </div>
        <div v-if="data.chart.length" class="mt-6 flex h-56 items-end gap-3 border-b border-line">
          <div v-for="(c, i) in data.chart" :key="i" class="flex flex-1 flex-col items-center gap-2">
            <div class="flex h-48 w-full items-end justify-center gap-1">
              <div class="w-1/3 rounded-t bg-primary" :class="{ 'opacity-60': i < data.chart.length - 1 }" :style="{ height: `${(c.pemasukan / max) * 100}%` }" :title="rupiah(c.pemasukan)" />
              <div class="w-1/3 rounded-t bg-red-400" :class="{ 'opacity-60': i < data.chart.length - 1 }" :style="{ height: `${(c.pengeluaran / max) * 100}%` }" :title="rupiah(c.pengeluaran)" />
            </div>
          </div>
        </div>
        <div class="mt-2 flex gap-3">
          <span v-for="(c, i) in data.chart" :key="i" class="flex-1 text-center text-xs" :class="i === data.chart.length - 1 ? 'font-semibold text-primary' : 'text-muted'">{{ c.label }}</span>
        </div>
        <p v-if="!data.chart.length" class="py-16 text-center text-sm text-muted">Belum ada data laporan.</p>
        <div class="mt-6 grid gap-4 border-t border-line pt-4 sm:grid-cols-2">
          <div>
            <p class="text-xs text-muted">Rata-rata Pemasukan Bulanan</p>
            <p class="font-bold">{{ rupiah(data.rataPemasukan) }}</p>
          </div>
          <div>
            <p class="text-xs text-muted">Rasio Efisiensi Belanja</p>
            <p class="font-bold" :class="data.rasioBelanja < 65 ? 'text-green-600' : 'text-red-600'">{{ data.rasioBelanja.toFixed(1) }}%</p>
            <p class="text-xs text-muted">Batas aman &lt; 65%</p>
          </div>
        </div>
      </section>

      <section class="card p-6">
        <h2 class="font-semibold">Aktivitas Terbaru</h2>
        <ol class="mt-4 space-y-5 border-l border-line pl-5">
          <li v-for="a in data.aktivitas" :key="a.id" class="relative">
            <span class="absolute -left-[27px] top-1 grid size-3.5 place-items-center rounded-full bg-primary ring-4 ring-white" />
            <p class="text-sm font-semibold">{{ a.judul }}</p>
            <p class="text-xs text-muted">{{ a.pesan }}</p>
            <p class="mt-1 text-xs text-slate-400">{{ waktuLalu(a.createdAt) }}</p>
          </li>
        </ol>
        <NuxtLink to="/notifikasi" class="btn-outline mt-6 w-full"><Bell class="size-4" /> Lihat Semua Aktivitas</NuxtLink>
      </section>
    </div>
  </div>
</template>
