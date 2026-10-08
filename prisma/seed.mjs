// Data awal sesuai design Figma. Aman dijalankan ulang (cek data dulu).
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()
const pw = process.env.SEED_ADMIN_PASSWORD
if (!pw || pw.length < 8) throw new Error('SEED_ADMIN_PASSWORD di .env wajib diisi (min 8 karakter)')

await prisma.user.upsert({
  where: { email: 'admin@bumdesmajujaya.desa.id' },
  update: {},
  create: {
    nama: 'Admin BUMDes', email: 'admin@bumdesmajujaya.desa.id', password: await bcrypt.hash(pw, 10),
    jabatan: 'Direktur Operasional', telepon: '+62 812-3456-7890', nik: '320409********01',
    unitKerja: 'Kantor Pengelola BUMDes Maju Jaya', role: 'SUPER_ADMIN',
  },
})

let b = await prisma.bumdes.findFirst()
if (!b) b = await prisma.bumdes.create({ data: {
  nama: 'BUMDes Maju Jaya', tahunBerdiri: 2021,
  dasarHukum: 'Perdes No. 04 Tahun 2021 & SK Kemenkumham RI AHU-00129',
  email: 'sekretariat@bumdesmajujaya.desa.id', telepon: '+62 812-3456-7890',
  alamat: 'Jl. Raya Desa Maju Jaya No. 12, Kec. Sukamaju, Kab. Makmur, Jawa Barat 40382',
  deskripsi: 'Menggerakkan Ekonomi Desa, Membangun Kesejahteraan Bersama',
  visi: 'Menjadi BUMDes mandiri, profesional, dan transparan yang menyejahterakan warga Desa Maju Jaya.',
  misi: '1. Mengoptimalkan potensi sumber daya alam dan kearifan lokal desa secara profesional dan lestari.\n2. Memberikan layanan utilitas air bersih, pariwisata edukatif, dan modernisasi alsintan pertanian yang terjangkau.\n3. Menerapkan tata kelola keuangan yang akuntabel, transparan, dan dapat diakses terbuka oleh warga desa.\n4. Membuka lapangan kerja produktif dan membina unit usaha mikro/UMKM desa.',
} })

if (!(await prisma.unitUsaha.count())) await prisma.unitUsaha.createMany({ data: [
  { bumdesId: b.id, nama: 'PAM Desa Tirta Jaya', kategori: 'Utilitas Air Bersih', penanggungJawab: 'Bpk. Suherman', kontak: '0812-1111-2222',
    deskripsi: 'Penyaluran air bersih layak konsumsi bersumber dari mata air alami pegunungan untuk kebutuhan sehari-hari warga 4 dusun.',
    metrikLabel: 'Omset Bulanan', metrikNilai: 'Rp 18.250.000/bln' },
  { bumdesId: b.id, nama: 'Desa Wisata Lembah Hijau', kategori: 'Pariwisata & Edukasi', penanggungJawab: 'Ibu Ratna Dewi', kontak: '0812-3333-4444',
    deskripsi: 'Pengembangan kawasan agro-wisata edukatif, tracking persawahan organik, dan spot kuliner olahan khas binaan ibu-ibu PKK.',
    metrikLabel: 'Tingkat Pengunjung', metrikNilai: '800+ Turis/Bln' },
  { bumdesId: b.id, nama: 'Sewa Alat & Mesin Pertanian', kategori: 'Modernisasi Pertanian', penanggungJawab: 'Bpk. Hendra Gunawan', kontak: '0812-5555-6666',
    deskripsi: 'Layanan persewaan traktor roda dua, mesin panen combine harvester, dan pompa air sawah dengan tarif sewa terjangkau petani.',
    metrikLabel: 'Kapasitas Cakupan', metrikNilai: '45 Hektar Sawah' },
] })

if (!(await prisma.laporanKeuangan.count())) await prisma.laporanKeuangan.createMany({ data: [
  [4, 12_400_000, 7_100_000, 'PUBLIK'], [5, 13_900_000, 7_600_000, 'PUBLIK'], [6, 15_200_000, 8_000_000, 'PUBLIK'],
  [7, 14_800_000, 7_900_000, 'DRAFT'], [8, 16_500_000, 8_100_000, 'PUBLIK'], [9, 18_250_000, 9_400_000, 'PUBLIK'],
].map(([bulan, inn, out, status]) => ({
  bumdesId: b.id, bulan, tahun: 2026, totalPemasukan: inn, totalPengeluaran: out, status,
  keterangan: 'Rekap pendapatan PAM Desa Tirta Jaya, Desa Wisata & sewa Alsintan.',
})) })

if (!(await prisma.aspirasi.count())) await prisma.aspirasi.createMany({ data: [
  { nama: 'Bpk. Mulyadi', kategori: 'PAM Desa (Tirta Jaya)', dusun: 'Dusun Karang Anyar', pesan: 'Debit air bersih PAM Desa Tirta Jaya mengalami penurunan tekanan di Dusun II.', status: 'MENUNGGU' },
  { nama: 'Ibu Siti Aminah', kategori: 'Desa Wisata', dusun: 'Dusun Sukarame', pesan: 'Usul penambahan papan petunjuk arah menuju Lembah Hijau.', status: 'DIPROSES' },
  { nama: 'Bpk. Darto', kategori: 'Sewa Alat Pertanian', dusun: 'Dusun Mekarsari', pesan: 'Jadwal sewa traktor saat musim tanam sering bentrok, mohon sistem antrean.', status: 'SELESAI', publik: true },
  { nama: 'Sdr. Rizki', kategori: 'Ide Usaha Baru', dusun: 'Dusun Krajan', pesan: 'Usul unit usaha bank sampah desa bekerja sama dengan karang taruna.', status: 'MENUNGGU' },
] })

if (!(await prisma.notifikasi.count())) await prisma.notifikasi.createMany({ data: [
  { tipe: 'audit', judul: 'Audit Semester I', pesan: 'Opini Wajar Tanpa Pengecualian dari Inspektorat Desa.', createdAt: new Date(Date.now() - 3 * 864e5) },
  { tipe: 'unit', judul: 'Unit Usaha PAM Desa', pesan: 'Pembaruan tarif meteran & kalibrasi pipa distribusi blok barat.', createdAt: new Date(Date.now() - 864e5) },
  { tipe: 'laporan', judul: 'Laporan Keuangan September 2026', pesan: 'Dokumen LPJ terverifikasi dan dirilis ke portal transparansi warga.', createdAt: new Date(Date.now() - 2 * 36e5) },
  { tipe: 'aspirasi', judul: 'Bpk. Mulyadi', pesan: 'Mengirim aspirasi baru terkait debit air PAM Desa.', createdAt: new Date(Date.now() - 10 * 6e4) },
] })

console.log('Seed selesai. Login: admin@bumdesmajujaya.desa.id / (SEED_ADMIN_PASSWORD)')
await prisma.$disconnect()
