-- CreateEnum
CREATE TYPE "Role" AS ENUM ('SUPER_ADMIN', 'ADMIN', 'PENGURUS');

-- CreateEnum
CREATE TYPE "StatusPublikasi" AS ENUM ('DRAFT', 'PUBLIK');

-- CreateEnum
CREATE TYPE "StatusAspirasi" AS ENUM ('MENUNGGU', 'DIPROSES', 'SELESAI');

-- CreateTable
CREATE TABLE "users" (
    "id" SERIAL NOT NULL,
    "nama" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "jabatan" TEXT,
    "telepon" TEXT,
    "nik" TEXT,
    "unit_kerja" TEXT,
    "avatar" TEXT,
    "role" "Role" NOT NULL DEFAULT 'ADMIN',
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "bumdes" (
    "id" SERIAL NOT NULL,
    "nama" TEXT NOT NULL,
    "tahun_berdiri" INTEGER,
    "dasar_hukum" TEXT,
    "email" TEXT,
    "telepon" TEXT,
    "alamat" TEXT,
    "deskripsi" TEXT,
    "visi" TEXT,
    "misi" TEXT,
    "logo" TEXT,

    CONSTRAINT "bumdes_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "unit_usaha" (
    "id" SERIAL NOT NULL,
    "bumdes_id" INTEGER NOT NULL,
    "nama" TEXT NOT NULL,
    "kategori" TEXT NOT NULL,
    "penanggung_jawab" TEXT NOT NULL,
    "kontak" TEXT NOT NULL,
    "deskripsi" TEXT,
    "foto" TEXT,
    "metrik_label" TEXT,
    "metrik_nilai" TEXT,
    "aktif" BOOLEAN NOT NULL DEFAULT true,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "unit_usaha_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "laporan_keuangan" (
    "id" SERIAL NOT NULL,
    "bumdes_id" INTEGER NOT NULL,
    "created_by" INTEGER,
    "bulan" INTEGER NOT NULL,
    "tahun" INTEGER NOT NULL,
    "total_pemasukan" INTEGER NOT NULL,
    "total_pengeluaran" INTEGER NOT NULL,
    "keterangan" TEXT,
    "file_lpj" TEXT,
    "status" "StatusPublikasi" NOT NULL DEFAULT 'DRAFT',
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "laporan_keuangan_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "aspirasi" (
    "id" SERIAL NOT NULL,
    "nama" TEXT NOT NULL,
    "kategori" TEXT NOT NULL,
    "whatsapp" TEXT,
    "dusun" TEXT,
    "pesan" TEXT NOT NULL,
    "status" "StatusAspirasi" NOT NULL DEFAULT 'MENUNGGU',
    "catatan_internal" TEXT,
    "publik" BOOLEAN NOT NULL DEFAULT false,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "aspirasi_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "notifikasi" (
    "id" SERIAL NOT NULL,
    "judul" TEXT NOT NULL,
    "pesan" TEXT NOT NULL,
    "tipe" TEXT NOT NULL,
    "dibaca" BOOLEAN NOT NULL DEFAULT false,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "notifikasi_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- CreateIndex
CREATE UNIQUE INDEX "laporan_keuangan_bumdes_id_bulan_tahun_key" ON "laporan_keuangan"("bumdes_id", "bulan", "tahun");

-- AddForeignKey
ALTER TABLE "unit_usaha" ADD CONSTRAINT "unit_usaha_bumdes_id_fkey" FOREIGN KEY ("bumdes_id") REFERENCES "bumdes"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "laporan_keuangan" ADD CONSTRAINT "laporan_keuangan_bumdes_id_fkey" FOREIGN KEY ("bumdes_id") REFERENCES "bumdes"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "laporan_keuangan" ADD CONSTRAINT "laporan_keuangan_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "users"("id") ON DELETE SET NULL ON UPDATE CASCADE;
