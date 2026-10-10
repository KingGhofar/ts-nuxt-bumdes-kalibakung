<script setup lang="ts">
const props = defineProps<{ status: string }>()
const map: Record<string, [string, string, string]> = {
  MENUNGGU: ['Menunggu', 'bg-amber-50 text-amber-800 ring-amber-200', 'bg-amber-500'],
  DIPROSES: ['Diproses', 'bg-blue-50 text-blue-800 ring-blue-200', 'bg-blue-600'],
  SELESAI: ['Selesai', 'bg-emerald-50 text-emerald-800 ring-emerald-200', 'bg-emerald-600'],
  PUBLIK: ['Tampil', 'bg-emerald-50 text-emerald-800 ring-emerald-200', 'bg-emerald-600'],
  DRAFT: ['Draft', 'bg-slate-100 text-slate-600 ring-slate-200', 'bg-slate-400'],
}
const v = computed(() => map[props.status] ?? [props.status, 'bg-slate-100 text-slate-600 ring-slate-200', 'bg-slate-400'])
</script>

<template>
  <span class="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full px-2.5 py-0.5 text-xs font-semibold ring-1" :class="v[1]">
    <span class="size-1.5 rounded-full" :class="v[2]" /> {{ v[0] }}
  </span>
</template>
