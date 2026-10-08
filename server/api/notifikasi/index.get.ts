export default defineEventHandler(async (event) => {
  const s = String(getQuery(event).q ?? '').trim()
  const [items, unread] = await Promise.all([
    prisma.notifikasi.findMany({
      where: s ? { OR: [{ judul: { contains: s, mode: 'insensitive' } }, { pesan: { contains: s, mode: 'insensitive' } }] } : {},
      orderBy: { createdAt: 'desc' }, take: 100,
    }),
    prisma.notifikasi.count({ where: { dibaca: false } }),
  ])
  return { items, unread }
})
