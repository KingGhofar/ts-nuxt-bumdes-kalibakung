<script setup lang="ts">
import { Mail, ShieldCheck, ArrowLeft } from 'lucide-vue-next'
definePageMeta({ layout: 'blank' })
useHead({ title: 'Verifikasi Email' })

const route = useRoute()
const brand = useBrand()
const status = ref<'loading' | 'ok' | 'error'>('loading')
const pesan = ref('')

async function verify() {
  const token = String(route.query.token ?? '')
  if (!token) { status.value = 'error'; pesan.value = 'Token tidak ditemukan di tautan.'; return }
  try {
    const r = await $fetch<{ message: string }>('/api/auth/verify', { method: 'POST', body: { token } })
    status.value = 'ok'; pesan.value = r.message
  } catch (e: any) {
    status.value = 'error'; pesan.value = e?.data?.statusMessage ?? 'Gagal memverifikasi email.'
  }
}
onMounted(verify)
</script>

<template>
  <main class="relative grid min-h-dvh place-items-center overflow-hidden bg-cover bg-center px-4 py-10" style="background-image: url('/bg-login.jpg')">
    <div class="absolute inset-0 bg-slate-900/25" aria-hidden="true" />
    <div class="relative w-full max-w-sm rounded-3xl border border-white/60 bg-gradient-to-b from-emerald-50/85 via-white/85 to-white/90 p-8 text-center shadow-2xl shadow-slate-900/30 backdrop-blur-md">
      <template v-if="status === 'loading'">
        <span class="mx-auto block size-8 animate-spin rounded-full border-2 border-slate-200 border-t-primary" />
        <p class="mt-4 text-sm text-muted">Memverifikasi email…</p>
      </template>
      <template v-else-if="status === 'ok'">
        <span class="mx-auto grid size-14 place-items-center rounded-full bg-emerald-100 text-emerald-700"><Mail class="size-6" /></span>
        <h1 class="mt-5 text-xl font-bold">Email Terverifikasi ✓</h1>
        <p class="mt-3 text-sm text-muted">{{ pesan }} Akun kamu akan aktif setelah disetujui admin {{ brand.nama }}.</p>
        <NuxtLink to="/login" class="mt-6 flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white py-2.5 text-sm font-medium shadow-sm hover:bg-slate-50"><ShieldCheck class="size-4" /> Ke Halaman Login</NuxtLink>
      </template>
      <template v-else>
        <span class="mx-auto grid size-14 place-items-center rounded-full bg-red-100 text-red-600"><ShieldCheck class="size-6" /></span>
        <h1 class="mt-5 text-xl font-bold">Verifikasi Gagal</h1>
        <p class="mt-3 text-sm text-muted">{{ pesan }}</p>
        <NuxtLink to="/publik" class="mt-6 flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white py-2.5 text-sm font-medium shadow-sm hover:bg-slate-50"><ArrowLeft class="size-4" /> Kembali ke Portal</NuxtLink>
      </template>
    </div>
  </main>
</template>
