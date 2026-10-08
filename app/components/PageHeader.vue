<script setup lang="ts">
import { ChevronRight } from 'lucide-vue-next'
defineProps<{ title: string, subtitle?: string, crumbs?: { label: string, to?: string }[] }>()
</script>

<template>
  <div class="mb-6 flex flex-wrap items-end justify-between gap-4">
    <div>
      <nav class="mb-2 flex items-center gap-1.5 text-xs text-muted" aria-label="Breadcrumb">
        <NuxtLink to="/dashboard" class="hover:text-primary">Dashboard</NuxtLink>
        <template v-for="c in crumbs" :key="c.label">
          <ChevronRight class="size-3" />
          <NuxtLink v-if="c.to" :to="c.to" class="hover:text-primary">{{ c.label }}</NuxtLink>
          <span v-else class="font-medium text-primary">{{ c.label }}</span>
        </template>
      </nav>
      <h1 class="text-2xl font-bold">{{ title }}</h1>
      <p v-if="subtitle" class="mt-1 text-sm text-muted">{{ subtitle }}</p>
    </div>
    <div class="flex flex-wrap gap-2"><slot /></div>
  </div>
</template>
