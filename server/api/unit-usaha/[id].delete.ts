export default defineEventHandler(async (event) => {
  await prisma.unitUsaha.delete({ where: { id: idParam(event) } })
  return { ok: true }
})
