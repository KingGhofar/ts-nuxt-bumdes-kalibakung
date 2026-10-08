import { randomUUID } from 'node:crypto'
import { mkdir, writeFile } from 'node:fs/promises'
import { extname, resolve } from 'node:path'

export const UPLOAD_DIR = resolve(process.cwd(), 'uploads')

const RULES = {
  image: { ext: ['.png', '.jpg', '.jpeg', '.svg', '.webp'], max: 2 * 1024 * 1024 },
  lpj: { ext: ['.pdf', '.xls', '.xlsx'], max: 10 * 1024 * 1024 },
} as const
export type UploadKind = keyof typeof RULES

// ponytail: validasi via ekstensi + ukuran, file disimpan di disk lokal dengan nama UUID (tak bisa ditebak).
// Upgrade ke cek magic-bytes + object storage (S3/MinIO) bila dipakai produksi skala besar.
export async function saveUpload(file: { filename?: string, data: Buffer }, kind: UploadKind) {
  const rule = RULES[kind]
  const ext = extname(file.filename ?? '').toLowerCase()
  if (!(rule.ext as readonly string[]).includes(ext))
    throw createError({ statusCode: 400, statusMessage: `Format file harus ${rule.ext.join(', ')}` })
  if (file.data.length > rule.max)
    throw createError({ statusCode: 400, statusMessage: `File melebihi ${rule.max / 1024 / 1024}MB` })
  await mkdir(UPLOAD_DIR, { recursive: true })
  const name = `${randomUUID()}${ext}`
  await writeFile(resolve(UPLOAD_DIR, name), file.data)
  return { name, original: file.filename }
}
