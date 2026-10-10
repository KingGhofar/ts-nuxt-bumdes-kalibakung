<script setup lang="ts">
// Tombol kecil unggah gambar (logo, avatar, foto pengurus).
import { UploadCloud } from 'lucide-vue-next'
const model = defineModel<string | null | undefined>()
defineProps<{ label?: string }>()
const { error } = useToast()
const busy = ref(false)
const input = ref<HTMLInputElement>()

async function pick(f?: File | null) {
  if (!f) return
  busy.value = true
  try { model.value = (await uploadFile(f, 'image')).name }
  catch (e) { error(e) }
  finally { busy.value = false; if (input.value) input.value.value = '' }
}
</script>

<template>
  <button type="button" class="btn-outline px-3 py-1.5 text-xs" :disabled="busy" @click="input?.click()">
    <UploadCloud class="size-4" /> {{ busy ? 'Mengunggah…' : (label ?? 'Ubah Foto') }}
  </button>
  <input ref="input" type="file" class="hidden" accept=".png,.jpg,.jpeg,.webp,.svg" @change="pick(($event.target as HTMLInputElement).files?.[0])">
</template>
