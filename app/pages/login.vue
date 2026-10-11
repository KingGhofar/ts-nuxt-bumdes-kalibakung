<script setup lang="ts">
import { Eye, EyeOff, Lock, Mail, LogIn, ArrowLeft } from 'lucide-vue-next'
definePageMeta({ layout: 'blank' })
useHead({ title: 'Masuk Pengurus' })

const brand = useBrand()
const { login } = useAuth()
const form = reactive({ email: '', password: '' })
const show = ref(false)
const err = ref('')
const busy = ref(false)

async function submit() {
  err.value = ''
  busy.value = true
  try { await login(form.email, form.password); await navigateTo('/dashboard') }
  catch (e: any) { err.value = e?.data?.statusMessage ?? 'Gagal masuk' }
  finally { busy.value = false }
}
</script>

<template>
  <main class="relative grid min-h-dvh place-items-center overflow-hidden bg-cover bg-center px-4 py-10" style="background-image: url('/bg-login.jpg')">
    <div class="absolute inset-0 bg-slate-900/25" aria-hidden="true" />

    <form class="relative w-full max-w-sm rounded-3xl border border-white/60 bg-gradient-to-b from-emerald-50/85 via-white/85 to-white/90 p-7 text-center shadow-2xl shadow-slate-900/30 backdrop-blur-md sm:p-8" @submit.prevent="submit">
      <h1 class="mt-5 text-xl font-bold">Masuk Pengurus</h1>
      <p class="mt-1.5 text-sm text-muted">Kelola laporan, unit usaha, dan aspirasi warga {{ brand.nama }}.</p>
      <div class="mt-6 space-y-2.5 text-left">
        <label class="relative block">
          <span class="sr-only">Email</span>
          <Mail class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-500" />
          <input v-model="form.email" type="email" autocomplete="username" required placeholder="Email" class="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm outline-none placeholder:text-slate-500 focus:border-primary focus:bg-white focus:ring-2 focus:ring-primary/20">
        </label>
        <label class="relative block">
          <span class="sr-only">Kata sandi</span>
          <Lock class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-500" />
          <input v-model="form.password" :type="show ? 'text' : 'password'" autocomplete="current-password" required placeholder="Kata sandi" class="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-10 text-sm outline-none placeholder:text-slate-500 focus:border-primary focus:bg-white focus:ring-2 focus:ring-primary/20">
          <button type="button" class="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 text-slate-500 hover:text-ink" :aria-label="show ? 'Sembunyikan sandi' : 'Tampilkan sandi'" @click="show = !show">
            <component :is="show ? EyeOff : Eye" class="size-4" />
          </button>
        </label>
      </div>

      <p v-if="err" class="mt-3 rounded-lg bg-red-50 px-3 py-2 text-left text-sm text-red-700" role="alert">{{ err }}</p>

      <button class="mt-5 w-full rounded-xl bg-gradient-to-b from-slate-700 to-slate-900 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-900/30 transition hover:from-slate-600 hover:to-slate-800 disabled:opacity-60" :disabled="busy">
        {{ busy ? 'Memproses…' : 'Masuk' }}
      </button>

      <div class="my-5 flex items-center gap-3 text-xs text-slate-500"><span class="h-px flex-1 border-t border-dashed border-slate-300" />atau<span class="h-px flex-1 border-t border-dashed border-slate-300" /></div>

      <NuxtLink to="/publik" class="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white py-2.5 text-sm font-medium shadow-sm hover:bg-slate-50">
        <ArrowLeft class="size-4" /> Kembali ke Portal Publik
      </NuxtLink>
    </form>
  </main>
</template>
