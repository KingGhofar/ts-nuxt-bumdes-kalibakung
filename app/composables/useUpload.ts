export async function uploadFile(file: File, kind: 'image' | 'lpj') {
  const fd = new FormData()
  fd.append('file', file)
  return $fetch<{ name: string, original: string }>(`/api/upload?kind=${kind}`, { method: 'POST', body: fd })
}

export const fileUrl = (name?: string | null) => (name ? `/files/${name}` : '')
