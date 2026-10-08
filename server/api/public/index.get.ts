export default defineEventHandler(async () => {
  const [bumdes, unit, laporan] = await Promise.all([
    prisma.bumdes.findFirst(),
    prisma.unitUsaha.findMany({ where: { aktif: true }, orderBy: { id: 'asc' } }),
    // Hanya laporan yang dipublikasikan.
    prisma.laporanKeuangan.findMany({ where: { status: 'PUBLIK' }, orderBy: [{ tahun: 'desc' }, { bulan: 'desc' }] }),
  ])
  return { bumdes, unit, laporan }
})
