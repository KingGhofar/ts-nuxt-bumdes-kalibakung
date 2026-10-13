<script setup lang="ts">
import { Mail, ArrowLeft, ShieldCheck } from 'lucide-vue-next'
definePageMeta({ layout: 'blank' })
useHead({ title: 'Kirim Ulang Verifikasi' })

const brand = useBrand()
const toast = useToast()
const email = ref('')
const busy = ref(false)
const done = ref(false)

async function submit() {
  busy.value = true
  try {
    const r = await $fetch<{ message: string }>('/api/auth/resend', { method: 'POST', body: { email: email.value } })
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
        <span class="mx-auto grid size-12 place-items-center rounded-xl bg-white text-ink shadow-md"><Mail class="size-5" /></span>
        <h1 class="mt-5 text-xl font-bold">Kirim Ulang Link Verifikasi</h1>
        <p class="mt-1.5 text-sm text-muted">Masukkan email yang kamu daftarkan. Kami kirim link verifikasi baru ke email itu.</p>

        <form class="mt-6 space-y-3 text-left" @submit.prevent="submit">
          <label class="relative block">
            <span class="sr-only">Email</span>
            <Mail class="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-slate-500" />
            <input v-model="email" type="email" required placeholder="Email" class="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm outline-none placeholder:text-slate-500 focus:border-primary focus:bg-white focus:ring-2 focus:ring-primary/20">
          </label>
          <button class="w-full rounded-xl bg-gradient-to-b from-slate-700 to-slate-900 py-3 text-sm font-semibold text-white shadow-lg shadow-slate-900/30 transition hover:from-slate-600 hover:to-slate-800 disabled:opacity-60" :disabled="busy">
            {{ busy ? 'Mengirim…' : 'Kirim Ulang Link' }}
          </button>
        </form>

        <div class="my-5 flex items-center gap-3 text-xs text-slate-500"><span class="h-px flex-1 border-t border-dashed border-slate-300" />atau<span class="h-px flex-1 border-t border-dashed border-slate-300" /></div>
        <NuxtLink to="/login" class="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white py-2.5 text-sm font-medium shadow-sm hover:bg-slate-50"><ArrowLeft class="size-4" /> Kembali ke Login</NuxtLink>
      </template>

      <template v-else>
        <span class="mx-auto grid size-14 place-items-center rounded-full bg-emerald-100 text-emerald-700"><ShieldCheck class="size-6" /></span>
        <h1 class="mt-5 text-xl font-bold">Cek Email Kamu</h1>
        <p class="mt-3 text-sm text-muted">Kalau email {{ email }} terdaftar dan belum terverifikasi, link baru sudah kami kirim. Periksa juga folder <b>Spam</b>.</p>
        <NuxtLink to="/login" class="mt-6 flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white py-2.5 text-sm font-medium shadow-sm hover:bg-slate-50">Ke Halaman Login</NuxtLink>
      </template>
    </div>
  </main>
</template>
