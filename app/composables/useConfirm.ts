type State = { open: boolean, title: string, text: string, ok: string, danger: boolean, resolve?: (v: boolean) => void }

export function useConfirm() {
  const s = useState<State>('confirm', () => ({ open: false, title: '', text: '', ok: 'OK', danger: false }))
  function ask(title: string, text: string, ok = 'Ya', danger = false) {
    return new Promise<boolean>(resolve => (s.value = { open: true, title, text, ok, danger, resolve }))
  }
  function answer(v: boolean) {
    s.value.resolve?.(v)
    s.value = { ...s.value, open: false }
  }
  return { state: s, ask, answer }
}
