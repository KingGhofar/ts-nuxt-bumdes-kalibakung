export default defineEventHandler(async (event) => {
  const id = idParam(event)
  return prisma.aspirasi.update({ where: { id }, data: await body(event, aspirasiAdminSchema) })
})
