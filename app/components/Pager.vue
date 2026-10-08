<script setup lang="ts">
const props = defineProps<{ total: number, size: number, label?: string }>()
const page = defineModel<number>({ required: true })
const pages = computed(() => Math.max(1, Math.ceil(props.total / props.size)))
const from = computed(() => (props.total ? (page.value - 1) * props.size + 1 : 0))
const to = computed(() => Math.min(page.value * props.size, props.total))
</script>

<template>
  <div class="flex flex-wrap items-center justify-between gap-3 border-t border-line px-4 py-4 text-sm">
    <p class="text-muted">Menampilkan {{ from }}-{{ to }} dari {{ total }} {{ label ?? 'data' }}</p>
    <div class="flex gap-1">
      <button class="btn-outline px-3 py-1.5" :disabled="page <= 1" @click="page--">‹ Sebelumnya</button>
      <button
        v-for="p in pages" :key="p" class="size-8 rounded-lg text-sm font-semibold"
        :class="p === page ? 'bg-primary text-white' : 'border border-line hover:bg-slate-50'" @click="page = p"
      >{{ p }}</button>
      <button class="btn-outline px-3 py-1.5" :disabled="page >= pages" @click="page++">Selanjutnya ›</button>
    </div>
  </div>
</template>
