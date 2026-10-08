<script setup lang="ts">
import { CheckCircle2, XCircle } from 'lucide-vue-next'
const { list } = useToast()
</script>

<template>
  <div class="fixed bottom-4 right-4 z-[60] space-y-2" aria-live="polite">
    <div
      v-for="t in list" :key="t.id"
      class="flex items-center gap-2 rounded-lg px-4 py-3 text-sm font-medium text-white shadow-lg"
      :class="t.type === 'success' ? 'bg-green-600' : 'bg-red-600'"
    >
      <component :is="t.type === 'success' ? CheckCircle2 : XCircle" class="size-4" /> {{ t.text }}
    </div>
  </div>
</template>
