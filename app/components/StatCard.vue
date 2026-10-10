<script setup lang="ts">
defineProps<{ label: string, value: string | number, note?: string, tone?: 'blue' | 'green' | 'red' | 'amber' | 'ink', icon?: any }>()
const tiles = {
  blue: 'bg-blue-50 text-primary', green: 'bg-emerald-50 text-emerald-600', red: 'bg-red-50 text-red-600',
  amber: 'bg-amber-50 text-amber-600', ink: 'bg-slate-100 text-slate-600',
}
const values = { blue: 'text-ink', green: 'text-emerald-700', red: 'text-red-600', amber: 'text-orange-600', ink: 'text-ink' }
</script>

<template>
  <div class="card flex min-w-0 flex-col p-5">
    <div class="flex items-start justify-between gap-3">
      <p class="text-[11px] font-semibold uppercase tracking-wider text-slate-600">{{ label }}</p>
      <span v-if="icon" class="grid size-9 shrink-0 place-items-center rounded-lg" :class="tiles[tone ?? 'blue']"><component :is="icon" class="size-[18px]" /></span>
    </div>
    <p class="mt-2 break-words text-2xl font-bold tracking-tight" :class="values[tone ?? 'blue']">{{ value }}</p>
    <div v-if="note || $slots.default" class="mt-auto pt-4">
      <div class="flex min-w-0 items-center gap-1.5 border-t border-slate-100 pt-3 text-xs text-muted">
        <slot>{{ note }}</slot>
      </div>
    </div>
  </div>
</template>
