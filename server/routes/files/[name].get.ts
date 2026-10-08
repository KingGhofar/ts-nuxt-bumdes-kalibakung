import { createReadStream } from 'node:fs'
import { stat } from 'node:fs/promises'
import { basename, extname, resolve } from 'node:path'

const TYPES: Record<string, string> = {
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.pdf': 'application/pdf', '.xls': 'application/vnd.ms-excel',
  '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}

export default defineEventHandler(async (event) => {
  const name = basename(getRouterParam(event, 'name') ?? '') // basename cegah path traversal
  const path = resolve(UPLOAD_DIR, name)
  try { await stat(path) } catch { throw createError({ statusCode: 404 }) }
  setHeader(event, 'Content-Type', TYPES[extname(name).toLowerCase()] ?? 'application/octet-stream')
  // SVG bisa berisi script: paksa sandbox.
  setHeader(event, 'Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; sandbox")
  setHeader(event, 'X-Content-Type-Options', 'nosniff')
  return sendStream(event, createReadStream(path))
})
