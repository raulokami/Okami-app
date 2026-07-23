import { AppHeader } from "@/components/app-header";
import { WeekForm } from "@/components/week-form";
import { prisma } from "@/lib/prisma";
import { requireRole } from "@/lib/require-role";
import { createWeek } from "@/app/weeks/actions";

export const dynamic = "force-dynamic";

export default async function GeneratePage() {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const athletes = await prisma.athlete.findMany({
    where: { organizationId: organization.id },
    orderBy: { name: "asc" },
    select: { id: true, name: true },
  });

  return (
    <>
      <AppHeader />
      <main className="flex flex-col gap-6 px-6 py-10">
        <div>
          <h1 className="font-heading text-2xl font-bold text-neutral-50">Generar semana</h1>
          <p className="mt-1 text-sm text-neutral-500">
            Pega el texto de la programacion y guardalo como borrador. Desde
            el detalle de la semana puedes generar el PDF real.
          </p>
        </div>
        <div className="max-w-xl">
          <WeekForm action={createWeek} athletes={athletes} submitLabel="Guardar borrador" />
        </div>
      </main>
    </>
  );
}
