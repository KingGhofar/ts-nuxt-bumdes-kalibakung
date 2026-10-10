// Identitas ringan untuk judul tab, sidebar, login.
export default defineEventHandler(async () => {
  const b = await prisma.bumdes.findFirst({ select: { nama: true, logo: true, alamat: true } })
  return b ?? { nama: 'BUMDes', logo: null, alamat: null }
})
