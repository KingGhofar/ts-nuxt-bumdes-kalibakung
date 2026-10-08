<script setup lang="ts">
import { Landmark } from 'lucide-vue-next'
definePageMeta({ layout: 'blank' })
useHead({ title: 'Masuk · BUMDes Maju Jaya' })

const { login } = useAuth()
const form = reactive({ email: '', password: '' })
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
  <div class="grid min-h-screen place-items-center p-4">
    <form class="card w-full max-w-sm p-8" @submit.prevent="submit">
      <div class="mb-6 flex items-center gap-3">
        <div class="grid size-11 place-items-center rounded-xl bg-primary text-white"><Landmark class="size-5" /></div>
        <div>
          <h1 class="font-bold">BUMDes Maju Jaya</h1>
          <p class="text-xs text-muted">Enterprise Console</p>
        </div>
      </div>
      <label class="label" for="email">Email</label>
      <input id="email" v-model="form.email" type="email" autocomplete="username" required class="input mb-4" placeholder="admin@bumdesmajujaya.desa.id">
      <label class="label" for="pw">Password</label>
      <input id="pw" v-model="form.password" type="password" autocomplete="current-password" required class="input">
      <p v-if="err" class="mt-3 text-sm text-red-600" role="alert">{{ err }}</p>
      <button class="btn-primary mt-6 w-full" :disabled="busy">{{ busy ? 'Memproses…' : 'Masuk' }}</button>
      <NuxtLink to="/publik" class="mt-4 block text-center text-xs text-muted hover:text-primary">Lihat Portal Transparansi Publik →</NuxtLink>
    </form>
  </div>
</template>
