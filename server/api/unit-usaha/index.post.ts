export default defineEventHandler(async (event) => {
  const data = await body(event, unitSchema)
  const b = await prisma.bumdes.findFirst()
  if (!b) throw createError({ statusCode: 400, statusMessage: 'Isi Profil BUMDes terlebih dahulu' })
  const unit = await prisma.unitUsaha.create({ data: { ...data, bumdesId: b.id } })
  await notify('unit', `Unit Usaha ${unit.nama}`, 'Unit usaha baru ditambahkan.')
  return unit
})
