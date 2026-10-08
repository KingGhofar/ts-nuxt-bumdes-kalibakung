<script setup lang="ts">
useHead({ title: 'Profil BUMDes · BUMDes Maju Jaya' })
const toast = useToast()
const { data } = await useFetch<any>('/api/bumdes')
const f = reactive({
  nama: '', tahunBerdiri: null as number | null, dasarHukum: '', email: '', telepon: '',
  alamat: '', deskripsi: '', visi: '', misi: '', logo: null as string | null,
})
if (data.value) Object.assign(f, Object.fromEntries(Object.entries(data.value).filter(([k]) => k in f)))
const busy = ref(false)

async function simpan() {
  busy.value = true
  try { await $fetch('/api/bumdes', { method: 'PUT', body: f }); toast.success('Profil BUMDes berhasil disimpan.') }
  catch (e) { toast.error(e) }
  finally { busy.value = false }
}
</script>

<template>
  <div>
    <PageHeader title="Kelola Profil BUMDes" subtitle="Identitas, legalitas, dan kontak resmi. Data ini ditampilkan di portal publik." :crumbs="[{ label: 'Profil BUMDes' }]" />
    <form class="card space-y-6 p-6" @submit.prevent="simpan">
      <div>
        <label class="label">Lambang Resmi BUMDes</label>
        <FileDrop v-model="f.logo" kind="image" accept=".png,.jpg,.jpeg,.svg,.webp" hint="Format PNG, JPG, atau SVG dengan rasio 1:1 (Maksimal 2MB)." />
      </div>
      <div class="grid gap-5 md:grid-cols-2">
        <div><label class="label" for="nama">Nama BUMDes *</label><input id="nama" v-model="f.nama" required class="input"></div>
        <div><label class="label" for="th">Tahun Berdiri</label><input id="th" v-model.number="f.tahunBerdiri" type="number" class="input"></div>
        <div class="md:col-span-2"><label class="label" for="dh">Dasar Hukum / Perdes &amp; SK Pengesahan</label><input id="dh" v-model="f.dasarHukum" class="input"></div>
        <div><label class="label" for="em">Email Kontak Resmi</label><input id="em" v-model="f.email" type="email" class="input"></div>
        <div><label class="label" for="tel">Nomor Telepon / WhatsApp</label><input id="tel" v-model="f.telepon" class="input"></div>
        <div class="md:col-span-2"><label class="label" for="al">Alamat Lengkap Kantor Sekretariat</label><input id="al" v-model="f.alamat" class="input"></div>
        <div class="md:col-span-2"><label class="label" for="ds">Slogan / Deskripsi Singkat</label><input id="ds" v-model="f.deskripsi" class="input"></div>
        <div class="md:col-span-2"><label class="label" for="vi">Visi</label><textarea id="vi" v-model="f.visi" rows="2" class="input" /></div>
        <div class="md:col-span-2"><label class="label" for="mi">Misi</label><textarea id="mi" v-model="f.misi" rows="5" class="input" /></div>
      </div>
      <div class="flex justify-end border-t border-line pt-5"><button class="btn-primary" :disabled="busy">Simpan Perubahan</button></div>
    </form>
  </div>
</template>
