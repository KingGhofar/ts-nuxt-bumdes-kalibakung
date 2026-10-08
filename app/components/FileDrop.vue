<script setup lang="ts">
import { UploadCloud, FileCheck2, X } from 'lucide-vue-next'

const props = defineProps<{ kind: 'image' | 'lpj', accept: string, hint: string }>()
const model = defineModel<string | null | undefined>()
const { error } = useToast()
const busy = ref(false)
const over = ref(false)
const input = ref<HTMLInputElement>()

async function pick(f?: File | null) {
  if (!f) return
  busy.value = true
  try { model.value = (await uploadFile(f, props.kind)).name }
  catch (e) { error(e) }
  finally { busy.value = false }
}
</script>

<template>
  <div
    class="rounded-xl border-2 border-dashed p-6 text-center transition"
    :class="over ? 'border-primary bg-blue-50' : 'border-line bg-slate-50'"
    @dragover.prevent="over = true" @dragleave="over = false"
    @drop.prevent="over = false; pick($event.dataTransfer?.files[0])"
  >
    <div v-if="model" class="flex items-center justify-center gap-3 text-sm">
      <img v-if="kind === 'image'" :src="fileUrl(model)" alt="" class="size-16 rounded-lg object-cover">
      <FileCheck2 v-else class="size-6 text-green-600" />
      <a :href="fileUrl(model)" target="_blank" class="font-medium text-primary underline">Lihat file</a>
      <button type="button" class="rounded p-1 text-muted hover:bg-slate-200" aria-label="Hapus file" @click="model = null"><X class="size-4" /></button>
    </div>
    <template v-else>
      <UploadCloud class="mx-auto size-8 text-muted" />
      <p class="mt-2 text-sm">Seret file ke sini atau <button type="button" class="font-semibold text-primary" @click="input?.click()">klik untuk memilih file</button></p>
      <p class="mt-1 text-xs text-muted">{{ hint }}</p>
      <button type="button" class="btn-outline mt-4" :disabled="busy" @click="input?.click()">{{ busy ? 'Mengunggah…' : 'Pilih Berkas Komputer' }}</button>
    </template>
    <input ref="input" type="file" class="hidden" :accept="accept" @change="pick(($event.target as HTMLInputElement).files?.[0])">
  </div>
</template>
