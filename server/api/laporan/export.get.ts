// Rekap CSV (dibuka langsung di Excel). ponytail: CSV, bukan .xlsx/PDF. Tambah lib xlsx/pdf bila butuh format resmi bertanda tangan.
export default defineEventHandler(async (event) => {
  const tahun = Number(getQuery(event).tahun) || undefined
  const rows = await prisma.laporanKeuangan.findMany({ where: tahun ? { tahun } : {}, orderBy: [{ tahun: 'asc' }, { bulan: 'asc' }] })
  const esc = (v: unknown) => `"${String(v ?? '').replaceAll('"', '""')}"`
  const csv = [
    ['Periode', 'Pemasukan', 'Pengeluaran', 'Saldo Bersih', 'Status', 'Keterangan'].join(';'),
    ...rows.map(r => [periode(r.bulan, r.tahun), r.totalPemasukan, r.totalPengeluaran, r.totalPemasukan - r.totalPengeluaran,
      r.status === 'PUBLIK' ? 'Tampil' : 'Draft', esc(r.keterangan)].join(';')),
  ].join('\r\n')
  setHeader(event, 'Content-Type', 'text/csv; charset=utf-8')
  setHeader(event, 'Content-Disposition', `attachment; filename="rekap-laporan-${tahun ?? 'semua'}.csv"`)
  return '\uFEFF' + csv // BOM agar Excel baca UTF-8
})
