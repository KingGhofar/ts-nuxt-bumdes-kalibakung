type User = { id: number, nama: string, email: string, jabatan: string | null, avatar: string | null, role: string }

export function useAuth() {
  const user = useState<User | null>('user', () => null)

  async function fetchMe() {
    try {
      // Saat SSR, teruskan cookie browser ke API.
      user.value = await $fetch<User>('/api/auth/me', { headers: useRequestHeaders(['cookie']) })
    } catch { user.value = null }
    return user.value
  }

  async function login(email: string, password: string) {
    const r = await $fetch<{ user: User }>('/api/auth/login', { method: 'POST', body: { email, password } })
    user.value = r.user
  }

  async function logout() {
    await $fetch('/api/auth/logout', { method: 'POST' })
    user.value = null
    await navigateTo('/login')
  }

  return { user, fetchMe, login, logout }
}
