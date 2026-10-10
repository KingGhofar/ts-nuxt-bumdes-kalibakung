export default defineEventHandler(() => prisma.bumdes.findFirst({ include: { pengurus: { orderBy: { urutan: 'asc' } } } }))
