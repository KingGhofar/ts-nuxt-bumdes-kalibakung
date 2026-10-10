<script setup lang="ts">
import { Landmark } from 'lucide-vue-next'
defineProps<{ size?: string, tone?: 'blue' | 'green' }>()
const brand = useBrand()
</script>

<template>
  <img v-if="brand.logo" :src="fileUrl(brand.logo)" alt="" class="shrink-0 rounded-xl object-cover" :class="size ?? 'size-10'">
  <span v-else class="grid shrink-0 place-items-center rounded-xl text-white" :class="[size ?? 'size-10', tone === 'green' ? 'bg-brand' : 'bg-primary']">
    <Landmark class="size-1/2" />
  </span>
</template>
