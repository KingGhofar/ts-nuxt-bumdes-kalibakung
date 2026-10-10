<script setup lang="ts">
const props = defineProps<{ total: number, size: number, label?: string }>()
const page = defineModel<number>({ required: true })
const pages = computed(() => Math.max(1, Math.ceil(props.total / props.size)))
const from = computed(() => (props.total ? (page.value - 1) * props.size + 1 : 0))
const to = computed(() => Math.min(page.value * props.size, props.total))
// Maksimal 5 tombol angka di sekitar halaman aktif.
const nums = computed(() => {
  const start = Math.max(1, Math.min(page.value - 2, pages.value - 4))
  return Array.from({ length: Math.min(5, pages.value) }, (_, i) => start + i)
})
</script>

<template>
  <div class="flex flex-col items-center justify-between gap-3 border-t border-line px-4 py-4 text-sm sm:flex-row">
    <p class="text-muted">Menampilkan <b class="text-ink">{{ from }}-{{ to }}</b> dari <b class="text-ink">{{ total }}</b> {{ label ?? 'data' }}</p>
    <div class="flex items-center gap-1">
      <button class="btn-outline px-3 py-1.5" :disabled="page <= 1" @click="page--">‹ <span class="hidden sm:inline">Sebelumnya</span></button>
      <button
        v-for="p in nums" :key="p" class="size-8 rounded-lg text-sm font-semibold"
        :class="p === page ? 'bg-primary text-white' : 'border border-line hover:bg-slate-50'" @click="page = p"
      >{{ p }}</button>
      <button class="btn-outline px-3 py-1.5" :disabled="page >= pages" @click="page++"><span class="hidden sm:inline">Selanjutnya</span> ›</button>
    </div>
  </div>
</template>
