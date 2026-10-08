export default defineEventHandler(async (event) => {
  const data = await body(event, laporanSchema)
  const b = await prisma.bumdes.findFirst()
  if (!b) throw createError({ statusCode: 400, statusMessage: 'Isi Profil BUMDes terlebih dahulu' })
  const dup = await prisma.laporanKeuangan.findUnique({ where: { bumdesId_bulan_tahun: { bumdesId: b.id, bulan: data.bulan, tahun: data.tahun } } })
  if (dup) throw createError({ statusCode: 409, statusMessage: `Laporan ${periode(data.bulan, data.tahun)} sudah ada` })
  return prisma.laporanKeuangan.create({ data: { ...data, bumdesId: b.id, createdById: requireUserId(event) } })
})
