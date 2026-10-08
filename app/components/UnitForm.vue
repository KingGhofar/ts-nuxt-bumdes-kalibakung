<script setup lang="ts">
const props = defineProps<{ initial?: any }>()
const emit = defineEmits<{ saved: [] }>()
const toast = useToast()
const KATEGORI = ['Utilitas Air Bersih', 'Pariwisata & Edukasi', 'Modernisasi Pertanian', 'Perdagangan', 'Jasa', 'Lainnya']
const f = reactive({
  nama: '', kategori: '', penanggungJawab: '', kontak: '', deskripsi: '',
  metrikLabel: '', metrikNilai: '', foto: null as string | null, ...pick(props.initial),
})
function pick(o?: any) {
  if (!o) return {}
  const { nama, kategori, penanggungJawab, kontak, deskripsi, metrikLabel, metrikNilai, foto } = o
  return { nama, kategori, penanggungJawab, kontak, deskripsi: deskripsi ?? '', metrikLabel: metrikLabel ?? '', metrikNilai: metrikNilai ?? '', foto }
}
const busy = ref(false)

async function simpan() {
  busy.value = true
  try {
    await $fetch(props.initial ? `/api/unit-usaha/${props.initial.id}` : '/api/unit-usaha', { method: props.initial ? 'PUT' : 'POST', body: f })
    toast.success('Unit usaha berhasil disimpan.')
    emit('saved')
  } catch (e) { toast.error(e) } finally { busy.value = false }
}
</script>

<template>
  <form class="card p-6" @submit.prevent="simpan">
    <div class="grid gap-5 md:grid-cols-2">
      <div><label class="label" for="n">Nama Unit Usaha *</label><input id="n" v-model="f.nama" required class="input" placeholder="Contoh: Pengelolaan Sampah & Bank Sampah Desa"></div>
      <div>
        <label class="label" for="k">Kategori Usaha *</label>
        <select id="k" v-model="f.kategori" required class="input">
          <option value="" disabled>Pilih kategori unit bisnis…</option>
          <option v-for="k in KATEGORI" :key="k">{{ k }}</option>
        </select>
      </div>
      <div><label class="label" for="pj">Nama Penanggung Jawab / Manajer Unit *</label><input id="pj" v-model="f.penanggungJawab" required class="input" placeholder="Nama lengkap penanggung jawab"></div>
      <div><label class="label" for="kt">Nomor Kontak / WhatsApp *</label><input id="kt" v-model="f.kontak" required class="input" placeholder="0812-xxxx-xxxx"></div>
      <div><label class="label" for="ml">Label Metrik Unggulan</label><input id="ml" v-model="f.metrikLabel" class="input" placeholder="Omset Bulanan"></div>
      <div><label class="label" for="mv">Nilai Metrik</label><input id="mv" v-model="f.metrikNilai" class="input" placeholder="Rp 18.250.000/bln"></div>
      <div class="md:col-span-2"><label class="label" for="d">Deskripsi Singkat Unit Usaha</label><textarea id="d" v-model="f.deskripsi" rows="4" class="input" placeholder="Tuliskan lingkup layanan, target penerima manfaat, dan lokasi operasional unit usaha…" /></div>
      <div class="md:col-span-2"><label class="label">Unggah Foto Utama Unit Usaha</label><FileDrop v-model="f.foto" kind="image" accept=".png,.jpg,.jpeg,.webp" hint="PNG/JPG, maksimal 2MB." /></div>
    </div>
    <div class="mt-6 flex justify-end gap-2 border-t border-line pt-5">
      <NuxtLink to="/unit-usaha" class="btn-outline">Batal</NuxtLink>
      <button class="btn-primary" :disabled="busy">Simpan Unit Usaha</button>
    </div>
  </form>
</template>
