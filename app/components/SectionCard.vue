<script setup lang="ts">
// Kartu dengan header ikon + judul + subjudul (pola berulang di Figma).
defineProps<{ title: string, subtitle?: string, icon?: any }>()
</script>

<template>
  <section class="card p-5 sm:p-6">
    <div class="flex flex-wrap items-start justify-between gap-3 border-b border-line pb-4">
      <div class="flex min-w-0 items-start gap-3">
        <span v-if="icon" class="grid size-10 shrink-0 place-items-center rounded-lg bg-blue-50 text-primary"><component :is="icon" class="size-5" /></span>
        <div class="min-w-0">
          <h2 class="font-semibold">{{ title }}</h2>
          <p v-if="subtitle" class="text-xs text-muted">{{ subtitle }}</p>
        </div>
      </div>
      <slot name="aside" />
    </div>
    <div class="pt-5"><slot /></div>
  </section>
</template>
