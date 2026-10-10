# BUMDes Desa Kalibakung — Sistem Informasi & Portal Transparansi

Desa Kalibakung, Kec. Balapulang, Kab. Tegal, Jawa Tengah.

Fullstack Nuxt 4 (frontend + backend Nitro) · Tailwind CSS v4 · Prisma · PostgreSQL · JWT.

## Setup (sekali)

1. Salin env lalu isi:
   ```bash
   cp .env.example .env
   ```
   - `DATABASE_URL` → ganti `PASSWORD` dengan password user `postgres` lokal.
   - `NUXT_JWT_SECRET` → string acak ≥ 32 karakter:
     `node -e "console.log(require('crypto').randomBytes(48).toString('hex'))"`
   - `SEED_ADMIN_PASSWORD` → password admin awal (≥ 8 karakter).

2. Install, buat database + tabel, isi data awal:
   ```bash
   npm install
   npx prisma migrate dev --name init  
   npm run db:seed
   ```

3. Jalankan:
   ```bash
   npm run dev
   ```
   Buka http://localhost:3000 → login `admin@kalibakung.desa.id` (atau `SEED_ADMIN_EMAIL`) + `SEED_ADMIN_PASSWORD`.
   Portal publik: http://localhost:3000/publik

## Struktur

```
app/
  layouts/default.vue      sidebar 5 menu + header (semua halaman admin)
  pages/                   1 file = 1 route
  components/              PageHeader, StatCard, ToggleSwitch, FileDrop, Pager, …
  middleware/auth.global   redirect ke /login bila belum login
server/
  api/                     REST: auth, bumdes, unit-usaha, laporan, aspirasi, notifikasi, akun, public
  middleware/auth.ts       semua /api/** wajib JWT kecuali /api/auth/login & /api/public
  utils/                   prisma, jwt, zod schema, upload
prisma/schema.prisma       ERD
uploads/                   file LPJ / foto (lokal, nama UUID)
```

## Route

| Route | Halaman |
|---|---|
| `/login` | Login |
| `/dashboard` | Ringkasan + grafik arus kas + aktivitas |
| `/profil-bumdes` | Identitas & legalitas |
| `/unit-usaha`, `/tambah`, `/:id`, `/:id/edit` | Unit usaha (card grid + toggle aktif) |
| `/laporan-keuangan`, `/tambah`, `/:id/edit` | Rekap kas bulanan + LPJ + toggle publikasi |
| `/aspirasi`, `/aspirasi/:id` | Aspirasi warga |
| `/notifikasi`, `/pengaturan`, `/bantuan` | Utilitas |
| `/publik` | Portal Transparansi (hanya laporan berstatus PUBLIK) |

## Data Desa Kalibakung

- `prisma/kalibakung.mjs` berisi identitas & unit usaha dari sumber publik (kalibakung.desa.id, balapulang.tegalkab.go.id,
  berita Maret 2026). Nama resmi BUMDes, SK/Perdes, tahun berdiri, visi-misi, pengurus, jam operasional, dan angka
  keuangan **belum ditemukan** — isi lewat menu Profil BUMDes, Unit Usaha, dan Laporan Keuangan.
- DB lama berisi contoh "Maju Jaya"? Jalankan sekali (tidak reset, hanya hapus baris contoh):
  ```bash
  node --env-file=.env prisma/ganti-ke-kalibakung.mjs
  ```


