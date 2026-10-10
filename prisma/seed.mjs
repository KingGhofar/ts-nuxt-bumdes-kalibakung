// Seed instalasi baru: akun admin + identitas BUMDes Desa Kalibakung + unit usaha.
// Laporan keuangan & aspirasi sengaja kosong (diinput pengurus). Aman dijalankan ulang.
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'
import { PROFIL, UNIT } from './kalibakung.mjs'

const prisma = new PrismaClient()
const pw = process.env.SEED_ADMIN_PASSWORD
if (!pw || pw.length < 8) throw new Error('SEED_ADMIN_PASSWORD di .env wajib diisi (min 8 karakter)')
const EMAIL = process.env.SEED_ADMIN_EMAIL || 'admin@kalibakung.desa.id'

await prisma.user.upsert({
  where: { email: EMAIL },
  update: {},
  create: { nama: 'Admin BUMDes', email: EMAIL, password: await bcrypt.hash(pw, 10), jabatan: 'Administrator', role: 'SUPER_ADMIN' },
})

let b = await prisma.bumdes.findFirst()
if (!b) b = await prisma.bumdes.create({ data: PROFIL })
if (!(await prisma.unitUsaha.count())) await prisma.unitUsaha.createMany({ data: UNIT.map(u => ({ ...u, bumdesId: b.id })) })

console.log(`Seed selesai. Login: ${EMAIL} / (SEED_ADMIN_PASSWORD)`)
await prisma.$disconnect()
