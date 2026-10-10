<script setup lang="ts">
import { Plus, Search, Store, CheckCircle2, Pencil, Trash2, Eye, PauseCircle } from 'lucide-vue-next'
useHead({ title: 'Unit Usaha' })
const toast = useToast()
const { ask } = useConfirm()
const q = ref('')
const { data, refresh } = await useFetch<any[]>('/api/unit-usaha', { query: { q } })
const aktif = computed(() => data.value?.filter(u => u.aktif).length ?? 0)
const total = computed(() => data.value?.length ?? 0)
const grad = ['from-sky-200 to-blue-100', 'from-emerald-200 to-green-100', 'from-amber-200 to-yellow-100', 'from-violet-200 to-indigo-100']

async function toggle(u: any, v: boolean) {
  try { await $fetch(`/api/unit-usaha/${u.id}`, { method: 'PUT', body: { aktif: v } }); u.aktif = v; toast.success(`Unit ${v ? 'ditampilkan' : 'disembunyikan'} di publik.`) }
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
    <PageHeader title="Manajemen Unit Usaha" subtitle="Kelola daftar layanan dan unit bisnis yang bernaung di bawah BUMDes." :crumbs="[{ label: 'Unit Usaha' }]">
      <NuxtLink to="/unit-usaha/tambah" class="btn-primary"><Plus class="size-4" /> Tambah Unit Usaha</NuxtLink>
    </PageHeader>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <StatCard label="Total Unit Usaha" :value="total" :icon="Store"><CheckCircle2 class="size-3.5 text-emerald-600" /> Terdaftar di sistem</StatCard>
      <StatCard label="Unit Usaha Aktif" :value="aktif" :icon="CheckCircle2" tone="green" :note="total ? `${Math.round(aktif / total * 100)}% dari portofolio unit aktif` : 'Belum ada unit'" />
      <StatCard label="Nonaktif" :value="total - aktif" :icon="PauseCircle" tone="ink" note="Tidak tampil di portal publik" />
    </div>

    <div class="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <h2 class="flex items-center gap-2 font-semibold">Portofolio Unit <span class="rounded-full bg-blue-100 px-2 py-0.5 text-xs font-bold text-blue-800">{{ total }} Ditampilkan</span></h2>
      <div class="relative sm:w-72">
        <Search class="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted" />
        <input v-model="q" class="input pl-9" placeholder="Cari layanan / unit usaha…" aria-label="Cari unit usaha">
      </div>
    </div>

    <div class="mt-4 grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-3">
      <article v-for="(u, i) in data" :key="u.id" class="card flex flex-col overflow-hidden transition hover:shadow-md">
        <div class="relative h-40 bg-gradient-to-br" :class="grad[i % grad.length]">
          <img v-if="u.foto" :src="fileUrl(u.foto)" alt="" class="size-full object-cover">
          <Store v-else class="absolute inset-0 m-auto size-12 text-white/80" />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-900/70 via-transparent to-transparent" />
          <span class="absolute left-3 top-3 inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold" :class="u.aktif ? 'bg-emerald-300 text-emerald-900' : 'bg-slate-200 text-slate-700'">
            <span class="size-1.5 rounded-full" :class="u.aktif ? 'bg-emerald-800' : 'bg-slate-500'" /> {{ u.aktif ? 'Aktif' : 'Nonaktif' }}
          </span>
          <span class="absolute right-3 top-3 rounded bg-white/85 px-2 py-0.5 font-mono text-[11px] font-semibold">ID: UNIT-{{ String(u.id).padStart(2, '0') }}</span>
          <p class="absolute bottom-3 left-4 right-4 truncate text-[11px] font-bold uppercase tracking-widest text-white">{{ u.kategori }}</p>
        </div>
        <div class="flex flex-1 flex-col p-5">
          <h3 class="font-semibold">{{ u.nama }}</h3>
          <p class="mt-1 line-clamp-2 text-sm text-muted">{{ u.deskripsi || 'Belum ada deskripsi.' }}</p>
          <dl v-if="u.penanggungJawab || u.metrikLabel" class="mt-4 grid grid-cols-2 gap-3 border-y border-line py-3 text-sm">
            <div class="min-w-0"><dt class="text-[11px] font-semibold text-muted">Penanggung Jawab</dt><dd class="truncate font-medium">{{ u.penanggungJawab || '—' }}</dd></div>
            <div class="min-w-0"><dt class="truncate text-[11px] font-semibold text-muted">{{ u.metrikLabel || 'Metrik' }}</dt><dd class="truncate font-semibold text-primary">{{ u.metrikNilai || '—' }}</dd></div>
          </dl>
          <NuxtLink v-else :to="`/unit-usaha/${u.id}/edit`" class="mt-4 block rounded-lg border border-dashed border-amber-300 bg-amber-50 px-3 py-2 text-xs font-medium text-amber-800 hover:bg-amber-100">Lengkapi penanggung jawab &amp; kontak →</NuxtLink>
          <div class="mt-auto flex items-center justify-between pt-4">
            <label class="flex items-center gap-2 text-xs font-semibold">
              <ToggleSwitch :model-value="u.aktif" :label="`Tampilkan ${u.nama} di publik`" @update:model-value="toggle(u, $event)" /> Tampil di Publik
            </label>
            <div class="flex">
              <NuxtLink :to="`/unit-usaha/${u.id}`" class="icon-btn" aria-label="Detail"><Eye class="size-4" /></NuxtLink>
              <NuxtLink :to="`/unit-usaha/${u.id}/edit`" class="icon-btn" aria-label="Edit"><Pencil class="size-4" /></NuxtLink>
              <button class="icon-btn text-red-500 hover:bg-red-50 hover:text-red-600" aria-label="Hapus" @click="hapus(u)"><Trash2 class="size-4" /></button>
            </div>
          </div>
        </div>
      </article>
    </div>
    <div v-if="!data?.length" class="card mt-4 p-10 text-center text-sm text-muted">
      Belum ada unit usaha. <NuxtLink to="/unit-usaha/tambah" class="font-semibold text-primary">Tambah sekarang →</NuxtLink>
    </div>
  </div>
</template>
