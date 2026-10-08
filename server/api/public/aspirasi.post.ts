// ponytail: tanpa rate-limit/captcha. Tambah (mis. limit per IP) bila mulai ada spam.
export default defineEventHandler(async (event) => {
  const data = await body(event, aspirasiPublikSchema)
  const a = await prisma.aspirasi.create({ data })
  await notify('aspirasi', `Aspirasi baru dari ${a.nama}`, a.pesan.slice(0, 160))
  return { ok: true }
})
