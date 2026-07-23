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

export async function createAthlete(formData: FormData) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const name = String(formData.get("name") ?? "").trim();
  const format = parseFormat(formData.get("format"));

  if (!name) {
    throw new Error("El nombre es obligatorio");
  }

  const athlete = await prisma.athlete.create({
    data: { organizationId: organization.id, name, format },
  });

  revalidatePath("/athletes");
  redirect(`/athletes/${athlete.id}`);
}

export async function updateAthlete(athleteId: string, formData: FormData) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const name = String(formData.get("name") ?? "").trim();
  const format = parseFormat(formData.get("format"));

  if (!name) {
    throw new Error("El nombre es obligatorio");
  }

  const { count } = await prisma.athlete.updateMany({
    where: { id: athleteId, organizationId: organization.id },
    data: { name, format },
  });

  if (count === 0) {
    notFound();
  }

  revalidatePath("/athletes");
  revalidatePath(`/athletes/${athleteId}`);
}

export async function deleteAthlete(athleteId: string) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  await prisma.athlete.deleteMany({
    where: { id: athleteId, organizationId: organization.id },
  });

  revalidatePath("/athletes");
  redirect("/athletes");
}
