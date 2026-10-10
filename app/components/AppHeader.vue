<script setup lang="ts">
import { Bell, HelpCircle, Search, Menu, Download, ChevronDown, LogOut, Settings, KeyRound, User, CalendarDays, ShieldCheck } from 'lucide-vue-next'

const emit = defineEmits<{ menu: [] }>()
const { user, logout } = useAuth()
const { data: unread } = useFetch('/api/notifikasi', { key: 'notif-count', transform: (r: any) => r.unread as number })
const q = ref('')
const open = ref(false)
const route = useRoute()
watch(() => route.fullPath, () => (open.value = false))
const initials = computed(() => user.value?.nama.split(' ').map(s => s[0]).slice(0, 2).join('').toUpperCase() ?? '?')

function cari() {
  if (q.value.trim()) navigateTo({ path: '/aspirasi', query: { q: q.value.trim() } })
}
</script>

<template>
  <header class="sticky top-0 z-20 flex h-16 items-center gap-2 border-b border-line bg-white/95 px-3 backdrop-blur sm:gap-3 sm:px-6 lg:px-8">
    <button class="icon-btn lg:hidden" aria-label="Buka menu" @click="emit('menu')"><Menu class="size-5" /></button>

    <form class="relative hidden max-w-md flex-1 md:block" role="search" @submit.prevent="cari">
      <Search class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
      <input v-model="q" class="input bg-slate-50 py-2 pl-9" placeholder="Cari aspirasi, pengirim, kata kunci…" aria-label="Pencarian">
    </form>

    <div class="ml-auto flex items-center gap-1 sm:gap-2">
      <span class="hidden items-center gap-1.5 rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1.5 text-xs font-semibold text-indigo-900 xl:inline-flex">
        <CalendarDays class="size-3.5" /> TA {{ new Date().getFullYear() }}
      </span>
      <a href="/api/laporan/export" class="btn hidden border border-blue-200 bg-blue-50 py-1.5 text-primary-hover hover:bg-blue-100 lg:inline-flex"><Download class="size-4" /> Unduh Rekap</a>
      <NuxtLink to="/notifikasi" class="icon-btn relative" aria-label="Notifikasi">
        <Bell class="size-5" />
        <span v-if="unread" class="absolute right-1 top-1 grid min-w-4 place-items-center rounded-full bg-red-500 px-1 text-[10px] font-bold leading-4 text-white ring-2 ring-white">{{ unread > 9 ? '9+' : unread }}</span>
      </NuxtLink>
      <NuxtLink to="/bantuan" class="icon-btn hidden sm:inline-grid" aria-label="Bantuan"><HelpCircle class="size-5" /></NuxtLink>
      <span class="mx-1 hidden h-8 w-px bg-line sm:block" />

      <div class="relative">
        <button class="flex items-center gap-2 rounded-full py-1 pl-1 pr-2 transition hover:bg-slate-100" :aria-expanded="open" aria-haspopup="menu" @click="open = !open">
          <img v-if="user?.avatar" :src="fileUrl(user.avatar)" alt="" class="size-9 rounded-full object-cover">
          <span v-else class="grid size-9 place-items-center rounded-full bg-blue-100 text-xs font-bold text-primary-hover">{{ initials }}</span>
          <span class="hidden text-left leading-tight md:block">
            <span class="block max-w-36 truncate text-sm font-semibold">{{ user?.nama }}</span>
            <span class="block max-w-36 truncate text-xs text-muted">{{ user?.jabatan }}</span>
          </span>
          <ChevronDown class="hidden size-4 text-muted sm:block" />
        </button>
        <template v-if="open">
          <div class="fixed inset-0 z-10" @click="open = false" />
          <div class="absolute right-0 z-20 mt-2 w-64 overflow-hidden rounded-xl border border-line bg-white shadow-xl" role="menu">
            <div class="border-b border-line px-4 py-3">
              <p class="truncate text-sm font-semibold">{{ user?.nama }}</p>
              <p class="truncate text-xs text-muted">{{ user?.email }}</p>
              <span v-if="user?.jabatan" class="mt-2 inline-flex items-center gap-1 rounded bg-blue-50 px-2 py-0.5 text-[11px] font-semibold text-primary"><ShieldCheck class="size-3" /> {{ user.jabatan }}</span>
            </div>
            <NuxtLink to="/pengaturan" class="flex items-center gap-2.5 px-4 py-2.5 text-sm hover:bg-slate-50" role="menuitem"><User class="size-4 text-muted" /> Lihat Profil</NuxtLink>
            <NuxtLink to="/pengaturan" class="flex items-center gap-2.5 px-4 py-2.5 text-sm hover:bg-slate-50" role="menuitem"><Settings class="size-4 text-muted" /> Pengaturan Akun</NuxtLink>
            <NuxtLink :to="{ path: '/pengaturan', query: { tab: 'keamanan' } }" class="flex items-center gap-2.5 px-4 py-2.5 text-sm hover:bg-slate-50" role="menuitem"><KeyRound class="size-4 text-muted" /> Ganti Kata Sandi</NuxtLink>
            <button class="flex w-full items-center gap-2.5 border-t border-line px-4 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50" role="menuitem" @click="logout"><LogOut class="size-4" /> Keluar (Logout)</button>
          </div>
        </template>
      </div>
    </div>
  </header>
</template>
