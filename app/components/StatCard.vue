<script setup lang="ts">
defineProps<{ label: string, value: string | number, note?: string, tone?: 'blue' | 'green' | 'red' | 'amber', icon?: any }>()
const tones = {
  blue: 'bg-blue-50 text-blue-600', green: 'bg-green-50 text-green-600',
  red: 'bg-red-50 text-red-600', amber: 'bg-amber-50 text-amber-600',
}
const values = { blue: 'text-ink', green: 'text-green-600', red: 'text-red-600', amber: 'text-ink' }
</script>

<template>
  <div class="card p-5">
    <div class="flex items-start justify-between">
      <p class="text-xs font-semibold uppercase tracking-wider text-muted">{{ label }}</p>
      <span v-if="icon" class="grid size-9 place-items-center rounded-lg" :class="tones[tone ?? 'blue']"><component :is="icon" class="size-4" /></span>
    </div>
    <p class="mt-3 text-2xl font-bold md:text-[28px]" :class="values[tone ?? 'blue']">{{ value }}</p>
    <p v-if="note" class="mt-3 border-t border-line pt-3 text-xs text-muted">{{ note }}</p>
  </div>
</template>
