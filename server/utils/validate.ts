import type { H3Event } from 'h3'
import type { ZodType } from 'zod'

export async function body<T>(event: H3Event, schema: ZodType<T>): Promise<T> {
  const r = schema.safeParse(await readBody(event))
  if (!r.success) throw createError({ statusCode: 400, statusMessage: r.error.issues[0]?.message ?? 'Input tidak valid' })
  return r.data
}

export function idParam(event: H3Event): number {
  const id = Number(getRouterParam(event, 'id'))
  if (!Number.isInteger(id) || id < 1) throw createError({ statusCode: 400, statusMessage: 'ID tidak valid' })
  return id
}
