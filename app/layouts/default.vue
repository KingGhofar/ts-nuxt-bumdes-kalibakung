<script setup lang="ts">
import { LayoutGrid, Building2, Store, FileBarChart, MessageSquareText, Settings, HelpCircle, LogOut, Plus, X, ShieldCheck } from 'lucide-vue-next'

const route = useRoute()
const brand = useBrand()
const { user, logout } = useAuth()
const isSuper = computed(() => user.value?.role === 'SUPER_ADMIN')
const { ask } = useConfirm()
const drawer = ref(false)
watch(() => route.fullPath, () => (drawer.value = false))

const menu = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutGrid },
  { to: '/profil-bumdes', label: 'Profil BUMDes', icon: Building2 },
  { to: '/unit-usaha', label: 'Unit Usaha', icon: Store },
  { to: '/laporan-keuangan', label: 'Laporan Keuangan', icon: FileBarChart },
  { to: '/aspirasi', label: 'Aspirasi Warga', icon: MessageSquareText },
  ...(isSuper.value ? [{ to: '/persetujuan-akun', label: 'Persetujuan Akun', icon: ShieldCheck }] : []),
]
const bottom = [
  { to: '/pengaturan', label: 'Pengaturan', icon: Settings },
  { to: '/bantuan', label: 'Bantuan', icon: HelpCircle },
]
const active = (to: string) => route.path === to || route.path.startsWith(to + '/')
const tahun = new Date().getFullYear()

async function keluar() {
  if (await ask('Keluar dari sistem?', 'Sesi login kamu akan diakhiri.', 'Keluar', true)) await logout()
}
</script>

<template>
  <div class="min-h-dvh bg-page font-sans text-ink">
    <div v-if="drawer" class="fixed inset-0 z-30 bg-slate-900/50 lg:hidden" aria-hidden="true" @click="drawer = false" />

    <aside
      class="fixed inset-y-0 left-0 z-40 flex w-[260px] flex-col overflow-y-auto bg-sidebar text-slate-400 transition-transform duration-200 lg:translate-x-0"
      :class="drawer ? 'translate-x-0' : '-translate-x-full'"
      aria-label="Sidebar"
    >
      <div class="flex items-center gap-3 px-5 pb-5 pt-6">
        <BrandMark />
        <div class="min-w-0">
          <p class="line-clamp-2 font-bold leading-tight text-white">{{ brand.nama }}</p>
          <p class="whitespace-nowrap text-[10px] font-semibold uppercase tracking-[0.12em]">Enterprise Console</p>
        </div>
        <button class="icon-btn ml-auto text-slate-400 hover:bg-white/10 hover:text-white lg:hidden" aria-label="Tutup menu" @click="drawer = false"><X class="size-5" /></button>
      </div>

      <div class="px-4">
        <NuxtLink to="/laporan-keuangan/tambah" class="btn-primary w-full py-2.5 shadow-lg shadow-blue-900/40"><Plus class="size-4" /> Tambah Laporan</NuxtLink>
      </div>

      <nav class="mt-6 flex-1 space-y-1 px-3" aria-label="Navigasi utama">
        <NuxtLink
          v-for="m in menu" :key="m.to" :to="m.to"
          class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition"
          :class="active(m.to) ? 'bg-primary text-white shadow-md shadow-blue-900/40' : 'hover:bg-white/5 hover:text-white'"
        >
          <component :is="m.icon" class="size-[18px] shrink-0" /> {{ m.label }}
        </NuxtLink>
      </nav>

      <div class="space-y-1 border-t border-white/10 px-3 py-4">
        <NuxtLink
          v-for="m in bottom" :key="m.to" :to="m.to"
          class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition"
          :class="active(m.to) ? 'bg-primary text-white' : 'hover:bg-white/5 hover:text-white'"
        >
          <component :is="m.icon" class="size-[18px] shrink-0" /> {{ m.label }}
        </NuxtLink>
        <button class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-red-400 transition hover:bg-red-500/10" @click="keluar">
          <LogOut class="size-[18px]" /> Keluar / Logout
        </button>
        <div class="mt-3 flex items-center justify-between rounded-lg border border-white/10 bg-white/5 px-3 py-2.5 text-xs">
          <span class="flex items-center gap-2 font-semibold text-white"><span class="size-2 rounded-full bg-green-500" /> Tahun Anggaran {{ tahun }}</span>
          <span class="text-[10px] font-bold uppercase tracking-wider text-green-400">Aktif</span>
        </div>
      </div>
    </aside>

    <div class="flex min-h-dvh flex-col lg:pl-[260px]">
      <AppHeader @menu="drawer = true" />
      <main class="mx-auto w-full max-w-[1200px] flex-1 px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
        <slot />
      </main>
      <footer class="border-t border-line px-4 py-5 text-center text-xs text-muted sm:px-8">
        © {{ tahun }} {{ brand.nama }}. Sistem Informasi Administrasi &amp; Tata Kelola Unit Usaha Desa.
      </footer>
    </div>
    <AppConfirm />
  </div>
</template>
