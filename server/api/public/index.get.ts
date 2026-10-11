export default defineEventHandler(async () => {
  const [bumdes, unit, laporan, aspirasi, aspirasiTotal, aspirasiSelesai] = await Promise.all([
    prisma.bumdes.findFirst({ include: { pengurus: { orderBy: { urutan: 'asc' } } } }),
    prisma.unitUsaha.findMany({ where: { aktif: true }, orderBy: { id: 'asc' } }),
    // Hanya laporan yang dipublikasikan.
    prisma.laporanKeuangan.findMany({ where: { status: 'PUBLIK' }, orderBy: [{ tahun: 'desc' }, { bulan: 'desc' }] }),
    // Hanya aspirasi yang ditandai publik oleh admin. WhatsApp tidak pernah dikirim ke publik.
    prisma.aspirasi.findMany({
      // ponytail: maks 20 terbaru (daftar di-scroll). Tambah paginasi bila perlu arsip lengkap.
      where: { publik: true }, orderBy: { createdAt: 'desc' }, take: 20,
      select: { id: true, nama: true, kategori: true, dusun: true, pesan: true, status: true, createdAt: true },
    }),
    prisma.aspirasi.count(),
    prisma.aspirasi.count({ where: { status: 'SELESAI' } }),
  ])
  return { bumdes, unit, laporan, aspirasi, stat: { aspirasiTotal, aspirasiSelesai } }
})
