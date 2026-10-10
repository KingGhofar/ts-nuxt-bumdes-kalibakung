export default defineEventHandler(async (event) => {
  const range = getQuery(event).range === 'tahun' ? 'tahun' : '6'
  const tahun = new Date().getFullYear()
  const [laporan, all, aspirasiMenunggu, unitAktif, unitNama, aktivitas] = await Promise.all([
    range === 'tahun'
      ? prisma.laporanKeuangan.findMany({ where: { tahun }, orderBy: { bulan: 'desc' } })
      : prisma.laporanKeuangan.findMany({ orderBy: [{ tahun: 'desc' }, { bulan: 'desc' }], take: 6 }),
    prisma.laporanKeuangan.aggregate({ _sum: { totalPemasukan: true, totalPengeluaran: true } }),
    prisma.aspirasi.count({ where: { status: 'MENUNGGU' } }),
    prisma.unitUsaha.count({ where: { aktif: true } }),
    prisma.unitUsaha.findMany({ where: { aktif: true }, select: { nama: true }, take: 4 }),
    prisma.notifikasi.findMany({ orderBy: { createdAt: 'desc' }, take: 4 }),
  ])
  const chart = laporan.reverse() // lama → baru
  const last = chart.at(-1)
  const prev = chart.at(-2)
  const laba = (l?: typeof last) => (l ? l.totalPemasukan - l.totalPengeluaran : 0)
  const totIn = chart.reduce((a, l) => a + l.totalPemasukan, 0)
  const totOut = chart.reduce((a, l) => a + l.totalPengeluaran, 0)
  return {
    saldoKas: (all._sum.totalPemasukan ?? 0) - (all._sum.totalPengeluaran ?? 0),
    labaBulanIni: laba(last),
    // Perubahan laba vs periode sebelumnya (%), null bila tak bisa dihitung.
    labaGrowth: prev && laba(prev) ? ((laba(last) - laba(prev)) / Math.abs(laba(prev))) * 100 : null,
    periodeTerakhir: last ? periode(last.bulan, last.tahun) : null,
    aspirasiMenunggu, unitAktif, unitNama: unitNama.map(u => u.nama),
    chart: chart.map(l => ({ label: BULAN[l.bulan - 1].slice(0, 3), pemasukan: l.totalPemasukan, pengeluaran: l.totalPengeluaran })),
    rataPemasukan: chart.length ? totIn / chart.length : 0,
    rasioBelanja: totIn ? (totOut / totIn) * 100 : 0,
    surplus: totIn - totOut,
    aktivitas,
  }
})
