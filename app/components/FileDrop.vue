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
  finally { busy.value = false; if (input.value) input.value.value = '' }
}
</script>

<template>
  <div
    class="rounded-xl border-2 border-dashed px-4 py-6 text-center transition"
    :class="over ? 'border-primary bg-blue-50' : 'border-slate-300 bg-slate-50/60'"
    @dragover.prevent="over = true" @dragleave="over = false"
    @drop.prevent="over = false; pick($event.dataTransfer?.files[0])"
  >
    <div v-if="model" class="flex flex-wrap items-center justify-center gap-3 text-sm">
      <img v-if="kind === 'image'" :src="fileUrl(model)" alt="" class="h-20 w-32 rounded-lg object-cover">
      <FileCheck2 v-else class="size-6 text-emerald-600" />
      <a :href="fileUrl(model)" target="_blank" class="font-medium text-primary underline">Lihat file</a>
      <button type="button" class="btn-outline px-3 py-1.5 text-xs" :disabled="busy" @click="input?.click()">Ganti</button>
      <button type="button" class="icon-btn size-8" aria-label="Hapus file" @click="model = null"><X class="size-4" /></button>
    </div>
    <template v-else>
      <span class="mx-auto grid size-12 place-items-center rounded-full bg-blue-100 text-primary"><UploadCloud class="size-6" /></span>
      <p class="mt-3 text-sm">Tarik dan lepas file ke sini, atau <button type="button" class="font-semibold text-primary hover:underline" @click="input?.click()">{{ busy ? 'mengunggah…' : 'Pilih Berkas Komputer' }}</button></p>
      <p class="mt-1 text-xs font-medium text-muted">{{ hint }}</p>
    </template>
    <input ref="input" type="file" class="hidden" :accept="accept" @change="pick(($event.target as HTMLInputElement).files?.[0])">
  </div>
</template>
