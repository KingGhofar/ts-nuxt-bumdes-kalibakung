<script setup lang="ts">
import { Eye, EyeOff, Lock, Mail, ArrowLeft } from 'lucide-vue-next'
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
  <div class="grid min-h-dvh lg:grid-cols-2">
    <div class="relative hidden overflow-hidden bg-sidebar p-12 text-white lg:flex lg:flex-col lg:justify-between">
      <div class="pointer-events-none absolute -left-24 -top-24 size-96 rounded-full bg-primary/30 blur-3xl" />
      <div class="pointer-events-none absolute -bottom-24 -right-24 size-96 rounded-full bg-emerald-500/20 blur-3xl" />
      <div class="relative flex items-center gap-3"><BrandMark /><div><p class="font-bold">{{ brand.nama }}</p><p class="text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-400">Enterprise Console</p></div></div>
      <div class="relative">
        <h1 class="font-display text-4xl font-extrabold leading-tight">Kelola BUMDes secara<br><span class="text-emerald-400">transparan &amp; akuntabel.</span></h1>
        <p class="mt-4 max-w-md text-slate-400">Rekap kas bulanan, unit usaha, dan aspirasi warga dalam satu sistem — langsung terhubung ke portal publik desa.</p>
      </div>
      <p class="relative text-xs text-slate-500">{{ brand.alamat }}</p>
    </div>

    <div class="flex flex-col justify-center px-5 py-10 sm:px-12">
      <form class="mx-auto w-full max-w-sm" @submit.prevent="submit">
        <div class="mb-8 flex items-center gap-3 lg:hidden"><BrandMark /><p class="font-bold">{{ brand.nama }}</p></div>
        <h2 class="text-2xl font-bold">Masuk Pengurus</h2>
        <p class="mt-1 text-sm text-muted">Gunakan akun yang diberikan administrator.</p>

        <label class="label mt-8" for="email">Email</label>
        <div class="relative">
          <Mail class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
          <input id="email" v-model="form.email" type="email" autocomplete="username" required class="input pl-9" placeholder="admin@desa.id">
        </div>
        <label class="label mt-4" for="pw">Kata Sandi</label>
        <div class="relative">
          <Lock class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
          <input id="pw" v-model="form.password" :type="show ? 'text' : 'password'" autocomplete="current-password" required class="input px-9">
          <button type="button" class="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-slate-400 hover:text-ink" :aria-label="show ? 'Sembunyikan sandi' : 'Tampilkan sandi'" @click="show = !show">
            <component :is="show ? EyeOff : Eye" class="size-4" />
          </button>
        </div>
        <p v-if="err" class="mt-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700" role="alert">{{ err }}</p>
        <button class="btn-primary mt-6 w-full py-3" :disabled="busy">{{ busy ? 'Memproses…' : 'Masuk' }}</button>
        <NuxtLink to="/publik" class="mt-6 flex items-center justify-center gap-1.5 text-sm text-muted hover:text-primary"><ArrowLeft class="size-4" /> Kembali ke Portal Publik</NuxtLink>
      </form>
    </div>
  </div>
</template>
