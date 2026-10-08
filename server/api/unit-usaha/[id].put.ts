export default defineEventHandler(async (event) => {
  const id = idParam(event)
  const data = await body(event, unitSchema.partial())
  return prisma.unitUsaha.update({ where: { id }, data })
})
