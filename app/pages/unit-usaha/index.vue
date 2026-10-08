<script setup lang="ts">
import { Plus, Search, Store, CheckCircle2, User, Pencil, Trash2, Eye } from 'lucide-vue-next'
useHead({ title: 'Unit Usaha · BUMDes Maju Jaya' })
const toast = useToast()
const { ask } = useConfirm()
const q = ref('')
const { data, refresh } = await useFetch<any[]>('/api/unit-usaha', { query: { q } })
const aktif = computed(() => data.value?.filter(u => u.aktif).length ?? 0)

async function toggle(u: any, v: boolean) {
  try { await $fetch(`/api/unit-usaha/${u.id}`, { method: 'PUT', body: { aktif: v } }); u.aktif = v; toast.success(`Unit ${v ? 'diaktifkan' : 'dinonaktifkan'}.`) }
  catch (e) { toast.error(e) }
}
async function hapus(u: any) {
  if (!(await ask('Hapus Unit Usaha?', `${u.nama} akan dihapus. Tindakan ini tidak dapat dibatalkan.`, 'Hapus', true))) return
  try { await $fetch(`/api/unit-usaha/${u.id}`, { method: 'DELETE' }); toast.success('Unit usaha dihapus.'); refresh() }
  catch (e) { toast.error(e) }
}
</script>

<template>
  <div>
    <PageHeader title="Manajemen Unit Usaha" subtitle="Kelola seluruh unit usaha BUMDes." :crumbs="[{ label: 'Unit Usaha' }]">
      <NuxtLink to="/unit-usaha/tambah" class="btn-primary"><Plus class="size-4" /> Tambah Unit Usaha</NuxtLink>
    </PageHeader>

    <div class="grid gap-4 sm:grid-cols-3">
      <StatCard label="Total Unit" :value="data?.length ?? 0" :icon="Store" />
      <StatCard label="Unit Aktif" :value="aktif" :icon="CheckCircle2" tone="green" :note="data?.length ? `${Math.round(aktif / data.length * 100)}% dari portofolio unit operasional aktif` : undefined" />
      <StatCard label="Nonaktif" :value="(data?.length ?? 0) - aktif" tone="red" />
    </div>

    <div class="relative mt-6 max-w-sm">
      <Search class="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
      <input v-model="q" class="input pl-9" placeholder="Cari layanan / unit usaha…" aria-label="Cari unit usaha">
    </div>

    <div class="mt-6 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
      <article v-for="u in data" :key="u.id" class="card flex flex-col overflow-hidden" :class="{ 'opacity-70': !u.aktif }">
        <div class="relative h-40 bg-gradient-to-br from-blue-100 to-slate-200">
          <img v-if="u.foto" :src="fileUrl(u.foto)" alt="" class="size-full object-cover">
          <Store v-else class="absolute inset-0 m-auto size-12 text-slate-400" />
          <div class="absolute left-3 top-3 flex gap-2">
            <span class="rounded-full bg-white/90 px-2.5 py-1 text-xs font-semibold text-primary backdrop-blur">{{ u.kategori }}</span>
            <span class="rounded-full px-2.5 py-1 text-xs font-semibold backdrop-blur" :class="u.aktif ? 'bg-green-500/90 text-white' : 'bg-slate-500/90 text-white'">{{ u.aktif ? 'Aktif' : 'Nonaktif' }}</span>
          </div>
        </div>
        <div class="flex flex-1 flex-col p-5">
          <h3 class="font-semibold">{{ u.nama }}</h3>
          <p class="mt-1 line-clamp-2 text-sm text-muted">{{ u.deskripsi }}</p>
          <dl class="mt-4 space-y-2 rounded-lg bg-slate-50 p-3 text-sm">
            <div class="flex justify-between"><dt class="flex items-center gap-1.5 text-muted"><User class="size-3.5" /> Penanggung Jawab</dt><dd class="font-medium">{{ u.penanggungJawab }}</dd></div>
            <div v-if="u.metrikLabel" class="flex justify-between"><dt class="text-muted">{{ u.metrikLabel }}</dt><dd class="font-semibold text-primary">{{ u.metrikNilai }}</dd></div>
          </dl>
          <div class="mt-auto flex items-center justify-between border-t border-line pt-4">
            <div class="flex items-center gap-2 text-xs text-muted">
              <ToggleSwitch :model-value="u.aktif" :label="`Status ${u.nama}`" @update:model-value="toggle(u, $event)" /> {{ u.aktif ? 'Aktif' : 'Nonaktif' }}
            </div>
            <div class="flex gap-1">
              <NuxtLink :to="`/unit-usaha/${u.id}`" class="rounded-lg p-2 text-muted hover:bg-slate-100" aria-label="Detail"><Eye class="size-4" /></NuxtLink>
              <NuxtLink :to="`/unit-usaha/${u.id}/edit`" class="rounded-lg p-2 text-muted hover:bg-slate-100" aria-label="Edit"><Pencil class="size-4" /></NuxtLink>
              <button class="rounded-lg p-2 text-red-500 hover:bg-red-50" aria-label="Hapus" @click="hapus(u)"><Trash2 class="size-4" /></button>
            </div>
          </div>
        </div>
      </article>
    </div>
    <p v-if="!data?.length" class="card mt-6 p-10 text-center text-sm text-muted">Belum ada unit usaha.</p>
  </div>
</template>
