import { notFound } from "next/navigation";
import { AppHeader } from "@/components/app-header";
import { DeleteButton } from "@/components/delete-button";
import { WeekForm } from "@/components/week-form";
import { WEEK_STATUS_LABEL } from "@/lib/format-labels";
import { prisma } from "@/lib/prisma";
import { requireRole } from "@/lib/require-role";
import { deleteWeek, updateWeek } from "@/app/weeks/actions";

export const dynamic = "force-dynamic";

export default async function WeekDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const [week, athletes] = await Promise.all([
    prisma.week.findFirst({
      where: { id: params.id, organizationId: organization.id },
    }),
    prisma.athlete.findMany({
      where: { organizationId: organization.id },
      orderBy: { name: "asc" },
      select: { id: true, name: true },
    }),
  ]);

  if (!week) {
    notFound();
  }

  const updateWithId = updateWeek.bind(null, week.id);
  const deleteWithId = deleteWeek.bind(null, week.id);

  return (
    <>
      <AppHeader />
      <main className="flex flex-col gap-6 px-6 py-10">
        <div className="flex items-center justify-between">
          <h1 className="font-heading text-2xl font-bold text-neutral-50">{week.semana}</h1>
          <span className="text-sm text-neutral-500">{WEEK_STATUS_LABEL[week.status]}</span>
        </div>

        {week.pdfUrl && (
          <a
            href={week.pdfUrl}
            target="_blank"
            rel="noreferrer"
            className="w-fit text-sm text-okami-accent hover:underline"
          >
            Ver PDF
          </a>
        )}

        <div className="max-w-xl">
          <WeekForm
            action={updateWithId}
            athletes={athletes}
            defaultAthleteId={week.athleteId}
            defaultFormat={week.format}
            defaultSubformato={week.subformato}
            defaultSemana={week.semana}
            defaultRawText={week.rawText}
            submitLabel="Guardar cambios"
          />
        </div>

        <DeleteButton
          action={deleteWithId}
          confirmMessage={`Borrar la semana "${week.semana}"?`}
        />
      </main>
    </>
  );
}
