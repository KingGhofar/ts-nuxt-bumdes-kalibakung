import { PrismaClient } from '@prisma/client'

// Satu instance; di dev disimpan di globalThis agar HMR tidak bikin koneksi baru terus.
const g = globalThis as unknown as { prisma?: PrismaClient }
export const prisma = g.prisma ?? new PrismaClient()
if (import.meta.dev) g.prisma = prisma
