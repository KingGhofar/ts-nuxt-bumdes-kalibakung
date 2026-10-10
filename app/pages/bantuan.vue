<script setup lang="ts">
import { BookOpen, MessageCircle, Wrench, ChevronDown, Bug, Landmark, Headset, HelpCircle, ShieldCheck, ExternalLink, CheckCircle2 } from 'lucide-vue-next'
useHead({ title: 'Bantuan' })
const brand = useBrand()
const { data: b } = await useFetch<any>('/api/bumdes')
const faq = [
  { q: 'Bagaimana cara mempublikasikan laporan keuangan?', steps: ['Buka menu Laporan Keuangan.', 'Aktifkan toggle "Publikasi" pada baris laporan.', 'Konfirmasi — laporan langsung tampil di Portal Publik.'] },
  { q: 'Bagaimana menindaklanjuti aspirasi warga?', steps: ['Buka menu Aspirasi Warga, pilih aspirasi.', 'Ubah status ke Diproses / Selesai dan tambah catatan internal.', 'Aktifkan "Tampilkan di Portal Publik" bila relevan.'] },
  { q: 'Berapa ukuran maksimal dokumen LPJ?', steps: ['Maksimal 10MB, format PDF atau Excel (.xls/.xlsx).', 'Foto unit/logo maksimal 2MB (PNG/JPG/WEBP/SVG).'] },
  { q: 'Bagaimana mengganti kata sandi admin?', steps: ['Buka Pengaturan → tab Keamanan & Autentikasi.', 'Isi kata sandi lama dan baru (min. 8 karakter), lalu simpan.'] },
]
const open = ref(0)
const wa = computed(() => b.value?.telepon ? `https://wa.me/${b.value.telepon.replace(/\D/g, '').replace(/^0/, '62')}` : null)
</script>

<template>
  <div>
    <PageHeader title="Bantuan &amp; Informasi Sistem" subtitle="Pusat bantuan admin dan detail versi perangkat lunak." :crumbs="[{ label: 'Bantuan' }]">
      <span class="inline-flex items-center gap-1.5 rounded-full border border-line bg-white px-3 py-1.5 text-xs"><span class="size-2 rounded-full bg-green-500" /> Sistem: <b class="text-emerald-700">Normal</b></span>
    </PageHeader>

    <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div class="min-w-0 space-y-6 lg:col-span-2">
        <SectionCard title="Pertanyaan Seputar Sistem (FAQ)" subtitle="Solusi kendala teknis dan alur administrasi mandiri." :icon="HelpCircle">
          <template #aside>
            <a v-if="wa" :href="wa" target="_blank" rel="noopener" class="inline-flex items-center gap-1.5 rounded-lg border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-semibold text-primary"><Headset class="size-4" /> Hubungi Helpdesk</a>
          </template>
          <div class="space-y-3">
            <div v-for="(f, i) in faq" :key="i" class="rounded-xl border transition" :class="open === i ? 'border-blue-300 shadow-sm shadow-blue-100' : 'border-line'">
              <button class="flex w-full items-center gap-3 p-4 text-left text-sm font-semibold" :aria-expanded="open === i" @click="open = open === i ? -1 : i">
                <span class="grid size-6 shrink-0 place-items-center rounded-md text-xs" :class="open === i ? 'bg-primary text-white' : 'bg-slate-100 text-slate-600'">{{ i + 1 }}</span>
                <span class="flex-1">{{ f.q }}</span>
                <ChevronDown class="size-4 shrink-0 transition" :class="open === i ? 'rotate-180 text-primary' : 'text-muted'" />
              </button>
              <ol v-if="open === i" class="grid gap-2 border-t border-line p-4 sm:grid-cols-3">
                <li v-for="(s, j) in f.steps" :key="j" class="flex gap-2 rounded-lg border border-line p-3 text-xs"><CheckCircle2 class="size-4 shrink-0 text-primary" /> {{ s }}</li>
              </ol>
            </div>
          </div>
        </SectionCard>

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div class="card p-5"><span class="grid size-10 place-items-center rounded-lg bg-blue-50 text-primary"><BookOpen class="size-5" /></span><p class="mt-3 font-semibold">Panduan Cepat</p><p class="text-sm text-muted">Baca FAQ di atas untuk alur pembukuan &amp; publikasi.</p></div>
          <div class="card p-5"><span class="grid size-10 place-items-center rounded-lg bg-emerald-50 text-emerald-700"><MessageCircle class="size-5" /></span><p class="mt-3 font-semibold">Kontak Darurat</p><p class="text-sm text-muted">Layanan WhatsApp kantor {{ brand.nama }}.</p>
            <a v-if="wa" :href="wa" target="_blank" rel="noopener" class="mt-2 inline-flex items-center gap-1 text-sm font-semibold text-emerald-700">Hubungi via WA <ExternalLink class="size-3.5" /></a></div>
          <div class="card p-5"><span class="grid size-10 place-items-center rounded-lg bg-indigo-50 text-indigo-600"><Wrench class="size-5" /></span><p class="mt-3 font-semibold">Pemeliharaan</p><p class="text-sm text-muted">Cadangkan database PostgreSQL secara berkala.</p></div>
        </div>
      </div>

      <div class="space-y-6">
        <section class="card p-5 text-center sm:p-6">
          <span class="mx-auto grid size-14 place-items-center rounded-2xl bg-primary text-white shadow-lg shadow-blue-200"><Landmark class="size-7" /></span>
          <h2 class="mt-4 font-bold">Sistem Informasi {{ brand.nama }}</h2>
          <span class="mt-2 inline-block rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-bold text-primary">v1.0.0</span>
          <p class="mt-3 text-sm text-muted">Platform akuntabilitas ekonomi desa, pengelolaan unit usaha, dan transparansi publik.</p>
          <dl class="mt-5 space-y-4 border-t border-line pt-5 text-left text-sm">
            <div><dt class="text-[11px] font-bold uppercase tracking-wider text-muted">Teknologi &amp; Ekosistem</dt>
              <dd class="mt-2 flex flex-wrap gap-1.5"><span v-for="t in ['Nuxt 4', 'Vue 3', 'Tailwind CSS', 'Prisma', 'PostgreSQL']" :key="t" class="rounded-md border border-line bg-slate-50 px-2 py-0.5 text-xs">{{ t }}</span></dd></div>
            <div><dt class="text-[11px] font-bold uppercase tracking-wider text-muted">Keamanan</dt><dd class="mt-1">JWT cookie httpOnly · bcrypt</dd></div>
          </dl>
          <a :href="b?.email ? `mailto:${b.email}?subject=Laporan%20Bug%20Sistem` : '#'" class="btn-outline mt-5 w-full"><Bug class="size-4 text-red-500" /> Laporkan Bug / Kendala</a>
        </section>
        <div class="flex items-start gap-3 rounded-xl border border-blue-200 bg-blue-50 p-4">
          <ShieldCheck class="size-6 shrink-0 text-primary" />
          <div><p class="text-sm font-semibold">Integritas Data</p><p class="text-xs text-muted">Hanya laporan berstatus Tampil yang terlihat publik.</p></div>
        </div>
      </div>
    </div>
  </div>
</template>
