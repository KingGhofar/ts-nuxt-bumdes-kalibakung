import { z } from 'zod'

export const unitSchema = z.object({
  nama: z.string().trim().min(1, 'Nama unit wajib diisi').max(200),
  kategori: z.string().trim().min(1, 'Kategori wajib dipilih').max(100),
  penanggungJawab: z.string().trim().min(1, 'Penanggung jawab wajib diisi').max(200),
  kontak: z.string().trim().min(1, 'Kontak wajib diisi').max(50),
  deskripsi: z.string().trim().max(2000).nullish(),
  foto: z.string().max(200).nullish(),
  metrikLabel: z.string().trim().max(100).nullish(),
  metrikNilai: z.string().trim().max(100).nullish(),
  aktif: z.boolean().optional(),
})

export const laporanSchema = z.object({
  bulan: z.coerce.number().int().min(1).max(12),
  tahun: z.coerce.number().int().min(2000).max(2100),
  totalPemasukan: z.coerce.number().int('Nominal tidak valid').min(0, 'Nominal tidak valid'),
  totalPengeluaran: z.coerce.number().int('Nominal tidak valid').min(0, 'Nominal tidak valid'),
  keterangan: z.string().trim().max(2000).nullish(),
  fileLpj: z.string().max(200).nullish(),
  status: z.enum(['DRAFT', 'PUBLIK']).optional(),
})

export const aspirasiPublikSchema = z.object({
  nama: z.string().trim().min(1, 'Nama wajib diisi').max(100),
  kategori: z.string().trim().min(1, 'Kategori wajib dipilih').max(100),
  whatsapp: z.string().trim().max(30).nullish(),
  dusun: z.string().trim().max(100).nullish(),
  pesan: z.string().trim().min(5, 'Pesan terlalu pendek').max(2000),
})

export const aspirasiAdminSchema = z.object({
  status: z.enum(['MENUNGGU', 'DIPROSES', 'SELESAI']).optional(),
  catatanInternal: z.string().trim().max(2000).nullish(),
  publik: z.boolean().optional(),
})
