<script setup lang="ts">
const { state, answer } = useConfirm()
</script>

<template>
  <div v-if="state.open" class="fixed inset-0 z-50 grid place-items-center bg-black/40 p-4" @click.self="answer(false)">
    <div class="card w-full max-w-md p-6" role="dialog" aria-modal="true">
      <h3 class="text-lg font-semibold">{{ state.title }}</h3>
      <p class="mt-2 text-sm text-muted">{{ state.text }}</p>
      <div class="mt-6 flex justify-end gap-2">
        <button class="btn-outline" @click="answer(false)">Batal</button>
        <button :class="state.danger ? 'btn-danger' : 'btn-primary'" @click="answer(true)">{{ state.ok }}</button>
      </div>
    </div>
  </div>
</template>
