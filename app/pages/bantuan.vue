<script setup lang="ts">
import { BookOpen, MessageCircle, Wrench, ChevronDown, Bug, Landmark } from 'lucide-vue-next'
useHead({ title: 'Bantuan · BUMDes Maju Jaya' })
const faq = [
  { q: 'Bagaimana cara menambah laporan keuangan bulanan?', steps: ['Buka menu Laporan Keuangan.', 'Klik "+ Tambah Laporan Bulanan".', 'Isi bulan, tahun, total pemasukan & pengeluaran.', 'Unggah file LPJ (opsional), lalu Simpan.'] },
  { q: 'Bagaimana laporan tampil di portal publik?', steps: ['Laporan baru berstatus Draft.', 'Aktifkan toggle "Status Publikasi" pada tabel laporan.', 'Konfirmasi, laporan tampil di halaman /publik.'] },
  { q: 'Bagaimana menindaklanjuti aspirasi warga?', steps: ['Buka menu Aspirasi Warga, klik Detail.', 'Ubah status ke Diproses / Selesai dan tambah catatan internal.', 'Aktifkan "Tampilkan di Portal Publik" bila perlu.'] },
]
const open = ref(0)
</script>

<template>
  <div>
    <PageHeader title="Bantuan &amp; Informasi Sistem" subtitle="Panduan penggunaan dan informasi teknis." :crumbs="[{ label: 'Bantuan' }]" />
    <div class="grid gap-6 lg:grid-cols-3">
      <section class="card p-6 lg:col-span-2">
        <h2 class="font-semibold">Pertanyaan Umum (FAQ)</h2>
        <div class="mt-4 divide-y divide-line">
          <div v-for="(f, i) in faq" :key="i" class="py-3">
            <button class="flex w-full items-center justify-between gap-4 text-left text-sm font-medium" :aria-expanded="open === i" @click="open = open === i ? -1 : i">
              {{ f.q }} <ChevronDown class="size-4 shrink-0 transition" :class="{ 'rotate-180': open === i }" />
            </button>
            <ol v-if="open === i" class="mt-3 list-decimal space-y-1 pl-5 text-sm text-muted"><li v-for="s in f.steps" :key="s">{{ s }}</li></ol>
          </div>
        </div>
      </section>
      <section class="card p-6">
        <div class="flex items-center gap-3">
          <span class="grid size-10 place-items-center rounded-xl bg-primary text-white"><Landmark class="size-5" /></span>
          <div><p class="font-semibold">BUMDes Maju Jaya</p><p class="text-xs text-muted">Enterprise Console v1.0.0</p></div>
        </div>
        <dl class="mt-5 space-y-3 text-sm">
          <div><dt class="text-xs font-semibold uppercase tracking-wider text-muted">Dikembangkan oleh</dt><dd>Divisi IT &amp; Pengembangan BUMDes</dd></div>
          <div><dt class="text-xs font-semibold uppercase tracking-wider text-muted">Teknologi</dt>
            <dd class="mt-1 flex flex-wrap gap-1.5"><span v-for="t in ['Nuxt 4', 'Tailwind CSS', 'Prisma', 'PostgreSQL']" :key="t" class="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs">{{ t }}</span></dd></div>
        </dl>
        <a href="mailto:sekretariat@bumdesmajujaya.desa.id?subject=Laporan%20Bug" class="btn-outline mt-6 w-full"><Bug class="size-4" /> Laporkan Bug</a>
      </section>
      <div class="grid gap-4 md:grid-cols-3 lg:col-span-3">
        <div class="card p-5"><BookOpen class="size-5 text-primary" /><p class="mt-3 font-semibold">Panduan Cepat</p><p class="text-sm text-muted">Modul SOP pembukuan kas &amp; penyerahan dividen.</p></div>
        <div class="card p-5"><MessageCircle class="size-5 text-green-600" /><p class="mt-3 font-semibold">Kontak Darurat</p><p class="text-sm text-muted">Layanan siaga WhatsApp Teknis Kantor Desa Maju Jaya.</p></div>
        <div class="card p-5"><Wrench class="size-5 text-amber-600" /><p class="mt-3 font-semibold">Jadwal Pemeliharaan</p><p class="text-sm text-muted">Pembersihan berkas log server setiap Sabtu pkl 23:00 WIB.</p></div>
      </div>
    </div>
  </div>
</template>
