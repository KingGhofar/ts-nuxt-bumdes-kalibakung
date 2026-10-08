type Toast = { id: number, type: 'success' | 'error', text: string }

export function useToast() {
  const list = useState<Toast[]>('toasts', () => [])
  function push(type: Toast['type'], text: string) {
    const id = Date.now() + Math.random()
    list.value.push({ id, type, text })
    setTimeout(() => (list.value = list.value.filter(t => t.id !== id)), 3500)
  }
  return {
    list,
    success: (t: string) => push('success', t),
    error: (e: unknown) => push('error', (e as any)?.data?.statusMessage || (e as any)?.statusMessage || (e as any)?.message || String(e)),
  }
}
