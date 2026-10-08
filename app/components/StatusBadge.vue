<script setup lang="ts">
const props = defineProps<{ status: string }>()
const map: Record<string, [string, string]> = {
  MENUNGGU: ['Menunggu', 'bg-amber-50 text-amber-700 ring-amber-200'],
  DIPROSES: ['Diproses', 'bg-blue-50 text-blue-700 ring-blue-200'],
  SELESAI: ['Selesai', 'bg-green-50 text-green-700 ring-green-200'],
  PUBLIK: ['Tampil', 'bg-green-50 text-green-700 ring-green-200'],
  DRAFT: ['Draft', 'bg-slate-100 text-slate-600 ring-slate-200'],
}
const v = computed(() => map[props.status] ?? [props.status, 'bg-slate-100 text-slate-600 ring-slate-200'])
</script>

<template>
  <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ring-1" :class="v[1]">{{ v[0] }}</span>
</template>
