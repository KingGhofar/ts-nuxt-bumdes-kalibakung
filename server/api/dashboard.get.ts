export default defineEventHandler(async () => {
  const [laporan, all, aspirasiMenunggu, unitAktif, aktivitas] = await Promise.all([
    prisma.laporanKeuangan.findMany({ orderBy: [{ tahun: 'desc' }, { bulan: 'desc' }], take: 6 }),
    prisma.laporanKeuangan.aggregate({ _sum: { totalPemasukan: true, totalPengeluaran: true } }),
    prisma.aspirasi.count({ where: { status: 'MENUNGGU' } }),
    prisma.unitUsaha.count({ where: { aktif: true } }),
    prisma.notifikasi.findMany({ orderBy: { createdAt: 'desc' }, take: 4 }),
  ])
  const chart = laporan.reverse() // lama → baru, untuk grafik
  const last = chart.at(-1)
  const n = chart.length || 1
  const rataPemasukan = chart.reduce((a, l) => a + l.totalPemasukan, 0) / n
  const totIn = chart.reduce((a, l) => a + l.totalPemasukan, 0)
  const totOut = chart.reduce((a, l) => a + l.totalPengeluaran, 0)
  return {
    saldoKas: (all._sum.totalPemasukan ?? 0) - (all._sum.totalPengeluaran ?? 0),
    labaBulanIni: last ? last.totalPemasukan - last.totalPengeluaran : 0,
    periodeTerakhir: last ? periode(last.bulan, last.tahun) : null,
    aspirasiMenunggu, unitAktif,
    chart: chart.map(l => ({ label: BULAN[l.bulan - 1], pemasukan: l.totalPemasukan, pengeluaran: l.totalPengeluaran })),
    rataPemasukan,
    rasioBelanja: totIn ? (totOut / totIn) * 100 : 0,
    aktivitas,
  }
})
