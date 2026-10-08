export default defineEventHandler(async (event) => {
  await prisma.aspirasi.delete({ where: { id: idParam(event) } })
  return { ok: true }
})
