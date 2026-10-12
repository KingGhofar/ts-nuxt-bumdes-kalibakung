<script setup lang="ts">
import { Eye, EyeOff, Lock, Mail, LogIn, ArrowLeft, ShieldCheck } from 'lucide-vue-next'
definePageMeta({ layout: 'blank' })
useHead({ title: 'Daftar Pengurus' })

const brand = useBrand()
const toast = useToast()
const form = reactive({ nama: '', email: '', password: '' })
const show = ref(false)
const busy = ref(false)
const done = ref(false)

async function submit() {
  busy.value = true
  try {
    const r = await $fetch<{ message: string }>('/api/auth/register', { method: 'POST', body: form })
    done.value = true
    toast.success(r.message)
  } catch (e) { toast.error(e) } finally { busy.value = false }
}
</script>

<template>
  <main class="relative grid min-h-dvh place-items-center overflow-hidden bg-cover bg-center px-4 py-10" style="background-image: url('/bg-login.jpg')">
    <div class="absolute inset-0 bg-slate-900/25" aria-hidden="true" />

    <div class="relative w-full max-w-sm rounded-3xl border border-white/60 bg-gradient-to-b from-emerald-50/85 via-white/85 to-white/90 p-7 text-center shadow-2xl shadow-slate-900/30 backdrop-blur-md sm:p-8">
      <template v-if="!done">
        <h1 class="mt-5 text-xl font-bold">Daftar Pengurus</h1>
        <p class="mt-1.5 text-sm text-muted">Daftar dengan Gmail, lalu verifikasi lewat email. Akun aktif setelah disetujui admin.</p>

        <form class="mt-6 space-y-2.5 text-left" @submit.prevent="submit">
          <label class="relative block">
            <span class="sr-only">Nama lengkap</span>
            <ShieldCheck class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-500" />
            <input v-model="form.nama" required minlength="2" maxlength="100" placeholder="Nama lengkap" class="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm outline-none placeholder:text-slate-500 focus:border-primary focus:bg-white focus:ring-2 focus:ring-primary/20">
          </label>
          <label class="relative block">
            <span class="sr-only">Email Gmail</span>
            <Mail class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-500" />
            <input v-model="form.email" type="email" required placeholder="Email Gmail" class="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm outline-none placeholder:text-slate-500 focus:border-primary focus:bg-white focus:ring-2 focus:ring-primary/20">
          </label>
          <label class="relative block">
            <span class="sr-only">Kata sandi</span>
            <Lock class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-500" />
            <input v-model="form.password" :type="show ? 'text' : 'password'" minlength="8" maxlength="100" required placeholder="Kata sandi (min. 8 karakter)" class="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-10 text-sm outline-none placeholder:text-slate-500 focus:border-primary focus:bg-white focus:ring-2 focus:ring-primary/20">
            <button type="button" class="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 text-slate-500 hover:text-ink" :aria-label="show ? 'Sembunyikan sandi' : 'Tampilkan sandi'" @click="show = !show">
              <component :is="show ? EyeOff : Eye" class="size-4" />
            </button>
          </label>
          <button class="mt-5 w-full rounded-xl bg-gradient-to-b from-slate-700 to-slate-900 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-900/30 transition hover:from-slate-600 hover:to-slate-800 disabled:opacity-60" :disabled="busy">
            {{ busy ? 'Mendaftar…' : 'Daftar' }}
          </button>
        </form>

        <div class="my-5 flex items-center gap-3 text-xs text-slate-500"><span class="h-px flex-1 border-t border-dashed border-slate-300" />atau<span class="h-px flex-1 border-t border-dashed border-slate-300" /></div>

        <div class="flex flex-col gap-2">
          <NuxtLink to="/login" class="w-full rounded-xl border border-slate-200 bg-white py-2.5 text-sm font-medium shadow-sm hover:bg-slate-50">Masuk</NuxtLink>
          <NuxtLink to="/publik" class="w-full rounded-xl border border-slate-200 bg-white py-2.5 text-sm font-medium shadow-sm hover:bg-slate-50">Kembali ke Portal Publik</NuxtLink>
        </div>
      </template>

      <template v-else>
        <span class="mx-auto grid size-14 place-items-center rounded-full bg-emerald-100 text-emerald-700"><Mail class="size-6" /></span>
        <h1 class="mt-5 text-xl font-bold">Cek Email Anda</h1>
        <p class="mt-3 text-sm text-muted">Kami kirim link verifikasi ke <b>{{ form.email }}</b>. Klik link tersebut dalam 24 jam untuk mengaktifkan akun. Setelah terverifikasi, akun masih menunggu persetujuan admin sebelum bisa login.</p>
        <NuxtLink to="/publik" class="mt-6 flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white py-2.5 text-sm font-medium shadow-sm hover:bg-slate-50"><ArrowLeft class="size-4" /> Kembali ke Portal Publik</NuxtLink>
      </template>
    </div>
  </main>
</template>
