export default defineEventHandler(async (event) => {
  const a = await prisma.aspirasi.findUnique({ where: { id: idParam(event) } })
  if (!a) throw createError({ statusCode: 404, statusMessage: 'Aspirasi tidak ditemukan' })
  return a
})
