export default defineEventHandler(async (event) => {
  const lap = await prisma.laporanKeuangan.findUnique({ where: { id: idParam(event) } })
  if (!lap) throw createError({ statusCode: 404, statusMessage: 'Laporan tidak ditemukan' })
  return lap
})
