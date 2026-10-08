export default defineEventHandler(async (event) => {
  const unit = await prisma.unitUsaha.findUnique({ where: { id: idParam(event) } })
  if (!unit) throw createError({ statusCode: 404, statusMessage: 'Unit usaha tidak ditemukan' })
  return unit
})
