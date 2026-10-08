export function notify(tipe: string, judul: string, pesan: string) {
  return prisma.notifikasi.create({ data: { tipe, judul, pesan } })
}
