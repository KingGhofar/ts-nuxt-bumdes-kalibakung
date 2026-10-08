import { SignJWT, jwtVerify } from 'jose'
import type { H3Event } from 'h3'

export const COOKIE = 'bumdes_token'
const TTL = 60 * 60 * 8 // 8 jam

function key() {
  const s = useRuntimeConfig().jwtSecret
  if (!s || s.length < 32) throw createError({ statusCode: 500, statusMessage: 'NUXT_JWT_SECRET belum diset (min 32 karakter)' })
  return new TextEncoder().encode(s)
}

export async function signToken(user: { id: number, role: string }) {
  return new SignJWT({ role: user.role })
    .setProtectedHeader({ alg: 'HS256' })
    .setSubject(String(user.id))
    .setIssuedAt()
    .setExpirationTime(`${TTL}s`)
    .sign(key())
}

// ponytail: hanya access token di cookie httpOnly (8 jam), tanpa refresh token. Tambah refresh bila sesi panjang diperlukan.
export function setAuthCookie(event: H3Event, token: string) {
  setCookie(event, COOKIE, token, { httpOnly: true, sameSite: 'lax', secure: !import.meta.dev, path: '/', maxAge: TTL })
}

export async function readUserId(event: H3Event): Promise<number | null> {
  const t = getCookie(event, COOKIE) || getHeader(event, 'authorization')?.replace(/^Bearer /, '')
  if (!t) return null
  try {
    const { payload } = await jwtVerify(t, key())
    return Number(payload.sub)
  } catch { return null }
}

export function requireUserId(event: H3Event): number {
  const id = event.context.userId as number | undefined
  if (!id) throw createError({ statusCode: 401, statusMessage: 'Belum login' })
  return id
}
