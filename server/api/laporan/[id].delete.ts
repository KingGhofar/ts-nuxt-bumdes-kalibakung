export default defineEventHandler(async (event) => {
  await prisma.laporanKeuangan.delete({ where: { id: idParam(event) } })
  return { ok: true }
})
