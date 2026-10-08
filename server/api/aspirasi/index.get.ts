export default defineEventHandler(async (event) => {
  const q = getQuery(event)
  const s = String(q.q ?? '').trim()
  const page = Math.max(1, Number(q.page) || 1)
  const size = [10, 25, 50].includes(Number(q.size)) ? Number(q.size) : 10
  const status = ['MENUNGGU', 'DIPROSES', 'SELESAI'].includes(String(q.status)) ? String(q.status) as any : undefined
  const where = {
    ...(status && { status }),
    ...(q.kategori && { kategori: String(q.kategori) }),
    ...(s && { OR: [{ nama: { contains: s, mode: 'insensitive' as const } }, { pesan: { contains: s, mode: 'insensitive' as const } }] }),
  }
  const [items, total, grouped] = await Promise.all([
    prisma.aspirasi.findMany({ where, orderBy: { createdAt: 'desc' }, skip: (page - 1) * size, take: size }),
    prisma.aspirasi.count({ where }),
    prisma.aspirasi.groupBy({ by: ['status'], _count: true }),
  ])
  const c = Object.fromEntries(grouped.map(g => [g.status, g._count]))
  return {
    items, total, page, size,
    stat: { total: grouped.reduce((a, g) => a + g._count, 0), menunggu: c.MENUNGGU ?? 0, diproses: c.DIPROSES ?? 0, selesai: c.SELESAI ?? 0 },
  }
})
