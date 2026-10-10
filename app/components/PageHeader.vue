<script setup lang="ts">
import { ChevronRight } from 'lucide-vue-next'
defineProps<{ title: string, subtitle?: string, crumbs?: { label: string, to?: string }[] }>()
</script>

<template>
  <div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
    <div class="min-w-0">
      <nav class="mb-2 flex flex-wrap items-center gap-1.5 text-xs text-muted" aria-label="Breadcrumb">
        <NuxtLink to="/dashboard" class="hover:text-primary">Dashboard</NuxtLink>
        <template v-for="c in crumbs" :key="c.label">
          <ChevronRight class="size-3 shrink-0" />
          <NuxtLink v-if="c.to" :to="c.to" class="hover:text-primary">{{ c.label }}</NuxtLink>
          <span v-else class="font-semibold text-primary">{{ c.label }}</span>
        </template>
      </nav>
      <h1 class="text-2xl font-bold tracking-tight sm:text-[28px]">{{ title }}</h1>
      <p v-if="subtitle" class="mt-1 text-sm text-muted">{{ subtitle }}</p>
    </div>
    <div v-if="$slots.default" class="flex flex-wrap gap-2 sm:shrink-0 sm:justify-end"><slot /></div>
  </div>
</template>
