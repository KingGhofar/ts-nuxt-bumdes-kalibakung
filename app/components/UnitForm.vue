<script setup lang="ts">
import { Store, Save } from 'lucide-vue-next'
const props = defineProps<{ initial?: any }>()
const emit = defineEmits<{ saved: [] }>()
const toast = useToast()
const brand = useBrand()
const f = reactive({
  nama: '', kategori: '', penanggungJawab: '', kontak: '', deskripsi: '',
  metrikLabel: '', metrikNilai: '', foto: null as string | null,
})
if (props.initial) for (const k of Object.keys(f) as (keyof typeof f)[]) if (props.initial[k] != null) (f as any)[k] = props.initial[k]
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
  <form @submit.prevent="simpan">
    <SectionCard :title="initial ? 'Edit Data Unit Usaha' : 'Formulir Data Unit Usaha Baru'" :subtitle="`Tambahkan unit bisnis ke dalam ekosistem ${brand.nama}`" :icon="Store">
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">
        <div><label class="label" for="n">Nama Unit Usaha <span class="text-red-500">*</span></label><input id="n" v-model="f.nama" required class="input" placeholder="Contoh: Pengelolaan Sampah Desa"></div>
        <div>
          <label class="label" for="k">Kategori Usaha <span class="text-red-500">*</span></label>
          <select id="k" v-model="f.kategori" required class="input">
            <option value="" disabled>Pilih kategori unit bisnis…</option>
            <option v-for="k in KATEGORI_UNIT" :key="k">{{ k }}</option>
            <option v-if="f.kategori && !KATEGORI_UNIT.includes(f.kategori)">{{ f.kategori }}</option>
          </select>
        </div>
        <div><label class="label" for="pj">Penanggung Jawab / Manajer Unit <span class="text-red-500">*</span></label><input id="pj" v-model="f.penanggungJawab" required class="input" placeholder="Nama lengkap penanggung jawab"></div>
        <div><label class="label" for="kt">Nomor Kontak / WhatsApp <span class="text-red-500">*</span></label><input id="kt" v-model="f.kontak" type="tel" required class="input" placeholder="0812-xxxx-xxxx"></div>
        <div><label class="label" for="ml">Label Metrik Unggulan</label><input id="ml" v-model="f.metrikLabel" class="input" placeholder="Contoh: Pelanggan Aktif"></div>
        <div><label class="label" for="mv">Nilai Metrik</label><input id="mv" v-model="f.metrikNilai" class="input" placeholder="Contoh: 160+ Rumah"></div>
        <div class="sm:col-span-2">
          <div class="flex justify-between gap-2"><label class="label" for="d">Deskripsi Singkat Unit Usaha</label><span class="text-xs font-medium text-muted">{{ f.deskripsi.length }}/250</span></div>
          <textarea id="d" v-model="f.deskripsi" rows="3" maxlength="250" class="input" placeholder="Tuliskan lingkup layanan, target penerima manfaat, dan lokasi operasional…" />
        </div>
        <div class="sm:col-span-2">
          <label class="label">Unggah Foto Utama Unit Usaha</label>
          <FileDrop v-model="f.foto" kind="image" accept=".png,.jpg,.jpeg,.webp" hint="Format JPG, PNG (maks. 2MB). Rasio ideal 16:9 untuk kartu publik." />
        </div>
      </div>
      <div class="mt-6 flex flex-col-reverse gap-2 border-t border-line pt-5 sm:flex-row sm:justify-end">
        <NuxtLink to="/unit-usaha" class="btn-outline">Batal</NuxtLink>
        <button class="btn-primary" :disabled="busy"><Save class="size-4" /> Simpan Data Unit</button>
      </div>
    </SectionCard>
  </form>
</template>
