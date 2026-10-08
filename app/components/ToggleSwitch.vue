<script setup lang="ts">
const model = defineModel<boolean>({ required: true })
defineProps<{ label?: string, disabled?: boolean }>()
</script>

<template>
  <button
    type="button" role="switch" :aria-checked="model" :aria-label="label" :disabled="disabled"
    class="relative inline-flex h-5 w-10 shrink-0 rounded-full transition disabled:opacity-50"
    :class="model ? 'bg-green-500' : 'bg-slate-300'"
    @click="model = !model"
  >
    <span class="absolute top-0.5 size-4 rounded-full bg-white shadow transition-all" :class="model ? 'left-[22px]' : 'left-0.5'" />
  </button>
</template>
