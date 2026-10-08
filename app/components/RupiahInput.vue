<script setup lang="ts">
// Tampil "18.250.000", nilai model angka murni.
const model = defineModel<number>({ required: true })
const text = computed({
  get: () => (model.value ? model.value.toLocaleString('id-ID') : ''),
  set: (v: string) => (model.value = Number(v.replace(/\D/g, '')) || 0),
})
</script>

<template>
  <div class="relative">
    <span class="absolute left-3 top-1/2 -translate-y-1/2 text-sm font-semibold text-muted">Rp</span>
    <input v-model="text" inputmode="numeric" class="input pl-10" placeholder="0">
  </div>
</template>
