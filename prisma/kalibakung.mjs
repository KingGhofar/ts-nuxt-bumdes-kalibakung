// Data publik Desa Kalibakung (sumber: kalibakung.desa.id, balapulang.tegalkab.go.id,
// inspirasiline.com 31-03-2026, jadesta.kemenpar.go.id). Nama resmi BUMDes, SK, pengurus,
// dan angka keuangan TIDAK ditemukan → dikosongkan, diisi pengurus lewat dashboard.
export const PROFIL = {
  nama: 'BUMDes Desa Kalibakung',
  alamat: 'Jl. Raya Kalibakung-Guci RT 01 RW 03, Desa Kalibakung, Kecamatan Balapulang, Kabupaten Tegal, Jawa Tengah 52464',
  telepon: '0823-2944-0791',
  email: 'kalibakung.tegalkab@gmail.com',
  deskripsi: 'Wadah keterbukaan informasi dan pertanggungjawaban unit usaha milik warga Desa Kalibakung. Bersama mengelola potensi desa yang mandiri, akuntabel, dan berkelanjutan.',
  tahunBerdiri: null, dasarHukum: null, visi: null, misi: null, jamOperasional: null,
}

// Rencana empat sektor usaha BUMDes Kalibakung (Kades Mujiono, Maret 2026) + Wisata Kalimus.
// penanggungJawab/kontak/metrik dikosongkan: belum ada data resmi.
export const UNIT = [
  { nama: 'Pengelolaan Air Bersih', kategori: 'Utilitas Air Bersih',
    deskripsi: 'Memastikan ketersediaan air bersih bagi seluruh warga Desa Kalibakung.' },
  { nama: 'Pengelolaan Sampah', kategori: 'Pengelolaan Sampah',
    deskripsi: 'Mengolah sampah warga menjadi sumber daya bermanfaat seperti maggot dan paving.' },
  { nama: 'Sarana Olahraga Desa', kategori: 'Sarana Olahraga',
    deskripsi: 'Pengelolaan lapangan desa sebagai pusat interaksi warga, dengan rencana penambahan jogging track.' },
  { nama: 'Desa Wisata Kalimus', kategori: 'Pariwisata & Edukasi',
    deskripsi: 'Kawasan wisata di atas Tanah Kas Desa sejak 2018, di jalur utama menuju kawasan wisata Guci.' },
]
