<script setup lang="ts">
import { Check, X, ShieldCheck } from 'lucide-vue-next'
useHead({ title: 'Persetujuan Akun' })

const toast = useToast()
const { ask } = useConfirm()
const { data, refresh } = await useFetch<any[]>('/api/auth/pending')

async function setujui(u: any, approved: boolean) {
  const ok = approved
    ? await ask('Setujui Akun?', `${u.nama} (${u.email}) akan bisa login setelah disetujui.`, 'Setujui')
    : await ask('Tolak Akun?', `Akun ${u.email} akan ditolak dan tidak bisa login.`, 'Tolak', true)
  if (!ok) return
  try {
    await $fetch('/api/auth/approve', { method: 'POST', body: { id: u.id, approved } })
    toast.success(approved ? 'Akun disetujui.' : 'Akun ditolak.')
    refresh()
  } catch (e) { toast.error(e) }
}
</script>

<template>
  <div>
    <PageHeader title="Persetujuan Akun" subtitle="Setujui atau tolak pendaftaran pengurus yang sudah memverifikasi emailnya." :crumbs="[{ label: 'Persetujuan Akun' }]" />

    <section class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[560px]">
          <thead class="border-b border-line bg-slate-50">
            <tr><th class="th">Nama</th><th class="th">Email</th><th class="th">Jabatan</th><th class="th">Mendaftar</th><th class="th text-right">Aksi</th></tr>
          </thead>
          <tbody class="divide-y divide-line">
            <tr v-for="u in data" :key="u.id" class="hover:bg-slate-50/60">
              <td class="td font-medium">{{ u.nama }}</td>
              <td class="td">{{ u.email }}</td>
              <td class="td">{{ u.jabatan || '—' }}</td>
              <td class="td whitespace-nowrap text-xs">{{ tanggal(u.createdAt) }}</td>
              <td class="td">
                <div class="flex justify-end gap-1">
                  <button class="btn bg-emerald-600 px-3 py-1.5 text-white hover:bg-emerald-700" @click="setujui(u, true)"><Check class="size-4" /> Setujui</button>
                  <button class="btn-outline px-3 py-1.5 text-red-600 hover:bg-red-50" @click="setujui(u, false)"><X class="size-4" /> Tolak</button>
                </div>
              </td>
            </tr>
            <tr v-if="!data?.length">
              <td colspan="5" class="td py-12 text-center text-muted"><ShieldCheck class="mx-auto mb-2 size-8 text-slate-300" /> Tidak ada akun menunggu persetujuan.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>
