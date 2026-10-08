import type { UploadKind } from '../utils/upload'

export default defineEventHandler(async (event) => {
  const kind = getQuery(event).kind as UploadKind
  if (kind !== 'image' && kind !== 'lpj') throw createError({ statusCode: 400, statusMessage: 'kind harus image|lpj' })
  const file = (await readMultipartFormData(event))?.find(f => f.name === 'file')
  if (!file) throw createError({ statusCode: 400, statusMessage: 'File wajib diunggah' })
  return saveUpload(file, kind)
})
