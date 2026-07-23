-- CreateEnum
CREATE TYPE "Format" AS ENUM ('CLASE_METCON', 'CLASE_ENDURANCE', 'ATLETA', 'HYBRID', 'RECOMPOSICION', 'SISTEMA_INDIVIDUAL', 'HYROX_INDIVIDUAL');

-- CreateEnum
CREATE TYPE "WeekStatus" AS ENUM ('DRAFT', 'GENERATED', 'SENT');

-- CreateTable
CREATE TABLE "Athlete" (
    "id" TEXT NOT NULL,
    "organizationId" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "format" "Format" NOT NULL,
    "jotformData" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Athlete_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Week" (
    "id" TEXT NOT NULL,
    "athleteId" TEXT,
    "organizationId" TEXT NOT NULL,
    "format" "Format" NOT NULL,
    "subformato" TEXT,
    "semana" TEXT NOT NULL,
    "rawText" TEXT NOT NULL,
    "pdfUrl" TEXT,
    "status" "WeekStatus" NOT NULL DEFAULT 'DRAFT',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Week_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "Athlete_organizationId_idx" ON "Athlete"("organizationId");

-- CreateIndex
CREATE INDEX "Week_organizationId_idx" ON "Week"("organizationId");

-- CreateIndex
CREATE INDEX "Week_athleteId_idx" ON "Week"("athleteId");

-- AddForeignKey
ALTER TABLE "Athlete" ADD CONSTRAINT "Athlete_organizationId_fkey" FOREIGN KEY ("organizationId") REFERENCES "Organization"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Week" ADD CONSTRAINT "Week_athleteId_fkey" FOREIGN KEY ("athleteId") REFERENCES "Athlete"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Week" ADD CONSTRAINT "Week_organizationId_fkey" FOREIGN KEY ("organizationId") REFERENCES "Organization"("id") ON DELETE CASCADE ON UPDATE CASCADE;
