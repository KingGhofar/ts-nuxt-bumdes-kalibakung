export const BULAN = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

export const rupiah = (n: number) => 'Rp ' + Math.round(n).toLocaleString('id-ID')

export const persen = (n: number, digits = 1) => `${n.toLocaleString('id-ID', { maximumFractionDigits: digits, minimumFractionDigits: digits })}%`

export const periode = (bulan: number, tahun: number) => `${BULAN[bulan - 1]} ${tahun}`

export const tanggal = (d: string | Date) =>
  new Date(d).toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' })

export function waktuLalu(d: string | Date) {
  const s = (Date.now() - new Date(d).getTime()) / 1000
  if (s < 60) return 'baru saja'
  if (s < 3600) return `${Math.floor(s / 60)} menit yang lalu`
  if (s < 86400) return `${Math.floor(s / 3600)} jam yang lalu`
  if (s < 172800) return 'kemarin'
  return `${Math.floor(s / 86400)} hari yang lalu`
}
