// Sekali jalan: ubah DB yang masih berisi data contoh "Maju Jaya" ke identitas Desa Kalibakung
// TANPA reset. Hanya menghapus baris yang persis berasal dari seed contoh lama; data yang
// kamu input sendiri tidak disentuh. Akun admin dipertahankan (password tetap).
// Jalankan:  node --env-file=.env prisma/ganti-ke-kalibakung.mjs
import { PrismaClient } from '@prisma/client'
import { PROFIL, UNIT } from './kalibakung.mjs'

const prisma = new PrismaClient()
const CONTOH_UNIT = ['PAM Desa Tirta Jaya', 'Desa Wisata Lembah Hijau', 'Sewa Alat & Mesin Pertanian']
const CONTOH_ASPIRASI = ['Bpk. Mulyadi', 'Ibu Siti Aminah', 'Bpk. Darto', 'Sdr. Rizki']
const KET_CONTOH = 'Rekap pendapatan PAM Desa Tirta Jaya, Desa Wisata & sewa Alsintan.'

const log = []
await prisma.$transaction(async (tx) => {
  const b = await tx.bumdes.findFirst()
  if (b) {
    await tx.bumdes.update({ where: { id: b.id }, data: PROFIL })
    log.push('profil BUMDes → Desa Kalibakung')
  }
  const u = await tx.unitUsaha.deleteMany({ where: { nama: { in: CONTOH_UNIT } } })
  log.push(`unit contoh dihapus: ${u.count}`)
  if (b && !(await tx.unitUsaha.count()))
    log.push(`unit Kalibakung dibuat: ${(await tx.unitUsaha.createMany({ data: UNIT.map(x => ({ ...x, bumdesId: b.id })) })).count}`)
  const l = await tx.laporanKeuangan.deleteMany({ where: { keterangan: KET_CONTOH } })
  log.push(`laporan contoh dihapus: ${l.count}`)
  const a = await tx.aspirasi.deleteMany({ where: { nama: { in: CONTOH_ASPIRASI } } })
  log.push(`aspirasi contoh dihapus: ${a.count}`)
  const n = await tx.notifikasi.deleteMany({ where: { judul: { in: ['Audit Semester I', 'Unit Usaha PAM Desa', 'Laporan Keuangan September 2026', 'Bpk. Mulyadi'] } } })
  log.push(`notifikasi contoh dihapus: ${n.count}`)
  // Akun admin contoh: bersihkan identitas Maju Jaya. Email login & password TIDAK diubah
  // (ganti email sendiri lewat Pengaturan agar tidak terkunci).
  const users = await tx.user.findMany({ where: { unitKerja: { contains: 'Maju Jaya' } } })
  for (const x of users) {
    await tx.user.update({ where: { id: x.id }, data: { unitKerja: 'Kantor BUMDes Desa Kalibakung', nik: null, telepon: null, jabatan: 'Administrator' } })
    log.push(`akun ${x.email}: identitas dibersihkan (email & password tetap)`)
  }
})
console.log(log.join('\n'))
await prisma.$disconnect()
