-- AlterTable
ALTER TABLE "users" ADD COLUMN     "approved" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "email_verified" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "verify_token_expires" TIMESTAMP(3),
ADD COLUMN     "verify_token_hash" TEXT;
