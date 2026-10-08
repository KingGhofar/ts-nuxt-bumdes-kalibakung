export default defineEventHandler(async (event) => {
  const id = idParam(event)
  const data = await body(event, laporanSchema.partial())
  const lap = await prisma.laporanKeuangan.update({ where: { id }, data })
  if (data.status === 'PUBLIK')
    await notify('laporan', `Laporan Keuangan ${periode(lap.bulan, lap.tahun)}`, 'Laporan dipublikasikan ke Portal Transparansi Publik.')
  return lap
})
