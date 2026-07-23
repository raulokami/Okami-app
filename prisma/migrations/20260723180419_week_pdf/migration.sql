-- CreateTable
CREATE TABLE "WeekPdf" (
    "weekId" TEXT NOT NULL,
    "data" BYTEA NOT NULL,
    "mimeType" TEXT NOT NULL DEFAULT 'application/pdf',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "WeekPdf_pkey" PRIMARY KEY ("weekId")
);

-- AddForeignKey
ALTER TABLE "WeekPdf" ADD CONSTRAINT "WeekPdf_weekId_fkey" FOREIGN KEY ("weekId") REFERENCES "Week"("id") ON DELETE CASCADE ON UPDATE CASCADE;
