export default defineEventHandler(async () => {
  await prisma.notifikasi.updateMany({ where: { dibaca: false }, data: { dibaca: true } })
  return { ok: true }
})
