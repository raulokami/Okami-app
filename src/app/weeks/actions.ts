"use server";

import { notFound, redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { prisma } from "@/lib/prisma";
import { requireRole } from "@/lib/require-role";
import type { Format } from "@/generated/prisma/enums";

const FORMAT_VALUES: Format[] = [
  "CLASE_METCON",
  "CLASE_ENDURANCE",
  "ATLETA",
  "HYBRID",
  "RECOMPOSICION",
  "SISTEMA_INDIVIDUAL",
  "HYROX_INDIVIDUAL",
];

function parseFormat(value: FormDataEntryValue | null): Format {
  if (typeof value === "string" && FORMAT_VALUES.includes(value as Format)) {
    return value as Format;
  }
  throw new Error("Formato invalido");
}

async function resolveAthleteId(organizationId: string, formData: FormData) {
  const raw = String(formData.get("athleteId") ?? "").trim();
  if (!raw) return null;

  const athlete = await prisma.athlete.findFirst({
    where: { id: raw, organizationId },
    select: { id: true },
  });

  if (!athlete) {
    throw new Error("Atleta invalido");
  }

  return athlete.id;
}

function requiredField(formData: FormData, key: string) {
  const value = String(formData.get(key) ?? "").trim();
  if (!value) {
    throw new Error(`El campo ${key} es obligatorio`);
  }
  return value;
}

export async function createWeek(formData: FormData) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const athleteId = await resolveAthleteId(organization.id, formData);
  const format = parseFormat(formData.get("format"));
  const semana = requiredField(formData, "semana");
  const rawText = requiredField(formData, "rawText");
  const subformato = String(formData.get("subformato") ?? "").trim() || null;

  const week = await prisma.week.create({
    data: {
      organizationId: organization.id,
      athleteId,
      format,
      subformato,
      semana,
      rawText,
    },
  });

  revalidatePath("/weeks");
  if (athleteId) revalidatePath(`/athletes/${athleteId}`);
  redirect(`/weeks/${week.id}`);
}

export async function updateWeek(weekId: string, formData: FormData) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const athleteId = await resolveAthleteId(organization.id, formData);
  const format = parseFormat(formData.get("format"));
  const semana = requiredField(formData, "semana");
  const rawText = requiredField(formData, "rawText");
  const subformato = String(formData.get("subformato") ?? "").trim() || null;

  const { count } = await prisma.week.updateMany({
    where: { id: weekId, organizationId: organization.id },
    data: { athleteId, format, subformato, semana, rawText },
  });

  if (count === 0) {
    notFound();
  }

  revalidatePath("/weeks");
  revalidatePath(`/weeks/${weekId}`);
  if (athleteId) revalidatePath(`/athletes/${athleteId}`);
}

export async function deleteWeek(weekId: string) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  await prisma.week.deleteMany({
    where: { id: weekId, organizationId: organization.id },
  });

  revalidatePath("/weeks");
  redirect("/weeks");
}
