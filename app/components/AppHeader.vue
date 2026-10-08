<script setup lang="ts">
import { Bell, HelpCircle, Search, Menu, Download, ChevronDown, LogOut, Settings } from 'lucide-vue-next'

const emit = defineEmits<{ menu: [] }>()
const { user, logout } = useAuth()
const { data: notif } = useFetch('/api/notifikasi', { key: 'notif-count', transform: (r: any) => r.unread })
const q = ref('')
const open = ref(false)
const initials = computed(() => user.value?.nama.split(' ').map(s => s[0]).slice(0, 2).join('') ?? '?')

function cari() {
  if (q.value.trim()) navigateTo({ path: '/aspirasi', query: { q: q.value.trim() } })
}
</script>

<template>
  <header class="sticky top-0 z-20 flex h-16 items-center gap-3 border-b border-line bg-white px-4 md:px-8">
    <button class="lg:hidden" aria-label="Buka menu" @click="emit('menu')"><Menu class="size-5" /></button>
    <form class="relative hidden max-w-sm flex-1 md:block" @submit.prevent="cari">
      <Search class="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
      <input v-model="q" class="input pl-9" placeholder="Cari aspirasi, pengirim, kata kunci…" aria-label="Pencarian">
    </form>
    <div class="ml-auto flex items-center gap-2 md:gap-4">
      <a href="/api/laporan/export" class="btn-outline hidden border-primary/40 text-primary md:inline-flex"><Download class="size-4" /> Unduh Rekap</a>
      <NuxtLink to="/notifikasi" class="relative rounded-lg p-2 hover:bg-slate-100" aria-label="Notifikasi">
        <Bell class="size-5 text-muted" />
        <span v-if="notif" class="absolute right-1.5 top-1.5 size-2 rounded-full bg-red-500" />
      </NuxtLink>
      <NuxtLink to="/bantuan" class="rounded-lg p-2 hover:bg-slate-100" aria-label="Bantuan"><HelpCircle class="size-5 text-muted" /></NuxtLink>
      <div class="relative">
        <button class="flex items-center gap-2 rounded-full border border-line py-1 pl-1 pr-3 hover:bg-slate-50" @click="open = !open">
          <img v-if="user?.avatar" :src="fileUrl(user.avatar)" alt="" class="size-8 rounded-full object-cover">
          <span v-else class="grid size-8 place-items-center rounded-full bg-primary text-xs font-bold text-white">{{ initials }}</span>
          <span class="hidden text-left leading-tight md:block">
            <span class="block text-sm font-semibold">{{ user?.nama }}</span>
            <span class="block text-xs text-muted">{{ user?.jabatan }}</span>
          </span>
          <ChevronDown class="size-4 text-muted" />
        </button>
        <div v-if="open" class="absolute right-0 mt-2 w-60 overflow-hidden rounded-xl border border-line bg-white shadow-lg" @click="open = false">
          <div class="border-b border-line px-4 py-3">
            <p class="text-sm font-semibold">{{ user?.nama }}</p>
            <p class="text-xs text-muted">{{ user?.email }}</p>
          </div>
          <NuxtLink to="/pengaturan" class="flex items-center gap-2 px-4 py-2.5 text-sm hover:bg-slate-50"><Settings class="size-4" /> Pengaturan Akun</NuxtLink>
          <button class="flex w-full items-center gap-2 border-t border-line px-4 py-2.5 text-sm text-red-600 hover:bg-red-50" @click="logout"><LogOut class="size-4" /> Keluar</button>
        </div>
      </div>
    </div>
  </header>
</template>
