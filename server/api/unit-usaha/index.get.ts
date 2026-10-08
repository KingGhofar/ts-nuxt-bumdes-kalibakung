export default defineEventHandler(async (event) => {
  const q = String(getQuery(event).q ?? '').trim()
  return prisma.unitUsaha.findMany({
    where: q ? { OR: [{ nama: { contains: q, mode: 'insensitive' } }, { kategori: { contains: q, mode: 'insensitive' } }] } : {},
    orderBy: { id: 'asc' },
  })
})
