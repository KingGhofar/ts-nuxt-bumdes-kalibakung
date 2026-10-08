export default defineEventHandler(async (event) => {
  const q = getQuery(event)
  const tahun = Number(q.tahun) || undefined
  const page = Math.max(1, Number(q.page) || 1)
  const size = [10, 25, 50].includes(Number(q.size)) ? Number(q.size) : 10
  const where = { ...(tahun && { tahun }) }
  const [items, total, agg, all] = await Promise.all([
    prisma.laporanKeuangan.findMany({ where, orderBy: [{ tahun: 'desc' }, { bulan: 'desc' }], skip: (page - 1) * size, take: size }),
    prisma.laporanKeuangan.count({ where }),
    prisma.laporanKeuangan.aggregate({ where, _sum: { totalPemasukan: true, totalPengeluaran: true } }),
    prisma.laporanKeuangan.aggregate({ _sum: { totalPemasukan: true, totalPengeluaran: true } }),
  ])
  return {
    items, total, page, size,
    ringkasan: {
      pendapatan: agg._sum.totalPemasukan ?? 0,
      pengeluaran: agg._sum.totalPengeluaran ?? 0,
      // Saldo kas = akumulasi semua periode (bukan cuma tahun terpilih)
      saldoKas: (all._sum.totalPemasukan ?? 0) - (all._sum.totalPengeluaran ?? 0),
    },
  }
})
