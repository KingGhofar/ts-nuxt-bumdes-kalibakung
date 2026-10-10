-- AlterTable
ALTER TABLE "bumdes" ADD COLUMN     "jam_operasional" TEXT;

-- AlterTable
ALTER TABLE "unit_usaha" ALTER COLUMN "penanggung_jawab" DROP NOT NULL,
ALTER COLUMN "kontak" DROP NOT NULL;

-- CreateTable
CREATE TABLE "pengurus" (
    "id" SERIAL NOT NULL,
    "bumdes_id" INTEGER NOT NULL,
    "nama" TEXT NOT NULL,
    "jabatan" TEXT NOT NULL,
    "keterangan" TEXT,
    "foto" TEXT,
    "urutan" INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT "pengurus_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "pengurus" ADD CONSTRAINT "pengurus_bumdes_id_fkey" FOREIGN KEY ("bumdes_id") REFERENCES "bumdes"("id") ON DELETE CASCADE ON UPDATE CASCADE;
