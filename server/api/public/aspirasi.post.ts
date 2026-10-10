// ponytail: honeypot saja, tanpa rate-limit/captcha. Tambah limit per IP bila mulai ada spam.
export default defineEventHandler(async (event) => {
  const raw = await readBody(event)
  if (raw?.website) return { ok: true } // bot mengisi field tersembunyi: diam-diam abaikan
  const r = aspirasiPublikSchema.safeParse(raw)
  if (!r.success) throw createError({ statusCode: 400, statusMessage: r.error.issues[0]?.message ?? 'Input tidak valid' })
  const a = await prisma.aspirasi.create({ data: r.data })
  await notify('aspirasi', `Aspirasi baru dari ${a.nama}`, a.pesan.slice(0, 160))
  return { ok: true }
})
