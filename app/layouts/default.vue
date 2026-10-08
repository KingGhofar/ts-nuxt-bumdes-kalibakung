<script setup lang="ts">
import { LayoutGrid, Building2, Store, FileBarChart, MessageSquareText, Settings, HelpCircle, LogOut, Plus, Landmark, Menu, X } from 'lucide-vue-next'

const route = useRoute()
const { logout } = useAuth()
const { ask } = useConfirm()
const drawer = ref(false)
watch(() => route.path, () => (drawer.value = false))

const menu = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutGrid },
  { to: '/profil-bumdes', label: 'Profil BUMDes', icon: Building2 },
  { to: '/unit-usaha', label: 'Unit Usaha', icon: Store },
  { to: '/laporan-keuangan', label: 'Laporan Keuangan', icon: FileBarChart },
  { to: '/aspirasi', label: 'Aspirasi Warga', icon: MessageSquareText },
]
const bottom = [
  { to: '/pengaturan', label: 'Pengaturan', icon: Settings },
  { to: '/bantuan', label: 'Bantuan', icon: HelpCircle },
]
const active = (to: string) => route.path === to || route.path.startsWith(to + '/')

async function keluar() {
  if (await ask('Keluar dari sistem?', 'Sesi login kamu akan diakhiri.', 'Keluar', true)) await logout()
}
</script>

<template>
  <div class="min-h-screen bg-page font-sans text-ink">
    <!-- Overlay mobile -->
    <div v-if="drawer" class="fixed inset-0 z-30 bg-black/40 lg:hidden" @click="drawer = false" />

    <aside
      class="fixed inset-y-0 left-0 z-40 flex w-[260px] flex-col bg-sidebar text-slate-400 transition-transform lg:translate-x-0"
      :class="drawer ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="flex items-center gap-3 px-5 py-5">
        <div class="grid size-10 place-items-center rounded-xl bg-primary text-white"><Landmark class="size-5" /></div>
        <div>
          <p class="font-bold text-white">BUMDes Maju Jaya</p>
          <p class="text-xs">Enterprise Console</p>
        </div>
        <button class="ml-auto lg:hidden" aria-label="Tutup menu" @click="drawer = false"><X class="size-5" /></button>
      </div>

      <div class="px-4">
        <NuxtLink to="/laporan-keuangan/tambah" class="btn-primary w-full rounded-full"><Plus class="size-4" /> Tambah Laporan</NuxtLink>
      </div>

      <nav class="mt-6 flex-1 space-y-1 px-3" aria-label="Navigasi utama">
        <NuxtLink
          v-for="m in menu" :key="m.to" :to="m.to"
          class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition"
          :class="active(m.to) ? 'bg-primary text-white' : 'hover:bg-white/5 hover:text-white'"
        >
          <component :is="m.icon" class="size-[18px]" /> {{ m.label }}
        </NuxtLink>
      </nav>

      <div class="space-y-1 border-t border-white/10 px-3 py-4">
        <NuxtLink
          v-for="m in bottom" :key="m.to" :to="m.to"
          class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition"
          :class="active(m.to) ? 'bg-primary text-white' : 'hover:bg-white/5 hover:text-white'"
        >
          <component :is="m.icon" class="size-[18px]" /> {{ m.label }}
        </NuxtLink>
        <button class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-red-400 hover:bg-red-500/10" @click="keluar">
          <LogOut class="size-[18px]" /> Keluar / Logout
        </button>
        <div class="mt-3 rounded-lg bg-white/5 px-3 py-3 text-xs">
          <p>Tahun Anggaran</p>
          <p class="mt-0.5 flex items-center gap-2 font-semibold text-white"><span class="size-2 rounded-full bg-green-500" /> {{ new Date().getFullYear() }} Aktif</p>
        </div>
      </div>
    </aside>

    <div class="lg:pl-[260px]">
      <AppHeader @menu="drawer = true" />
      <main class="mx-auto max-w-[1100px] p-4 md:p-8">
        <slot />
      </main>
      <footer class="flex flex-wrap justify-between gap-2 border-t border-line px-8 py-4 text-xs text-muted">
        <span>© {{ new Date().getFullYear() }} Pemerintah Desa Maju Jaya · BUMDes Maju Jaya Enterprise Console</span>
        <span>v1.0.0</span>
      </footer>
    </div>
    <AppConfirm />
  </div>
</template>
