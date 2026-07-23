import Link from "next/link";
import { notFound } from "next/navigation";
import { AppHeader } from "@/components/app-header";
import { AthleteForm } from "@/components/athlete-form";
import { DeleteButton } from "@/components/delete-button";
import { FORMAT_LABEL, WEEK_STATUS_LABEL } from "@/lib/format-labels";
import { prisma } from "@/lib/prisma";
import { requireRole } from "@/lib/require-role";
import { deleteAthlete, updateAthlete } from "@/app/athletes/actions";

export const dynamic = "force-dynamic";

export default async function AthleteDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const athlete = await prisma.athlete.findFirst({
    where: { id: params.id, organizationId: organization.id },
    include: { weeks: { orderBy: { createdAt: "desc" } } },
  });

  if (!athlete) {
    notFound();
  }

  const updateWithId = updateAthlete.bind(null, athlete.id);
  const deleteWithId = deleteAthlete.bind(null, athlete.id);

  return (
    <>
      <AppHeader />
      <main className="flex flex-col gap-10 px-6 py-10">
        <div className="max-w-sm">
          <h1 className="mb-6 font-heading text-2xl font-bold text-neutral-50">
            {athlete.name}
          </h1>
          <AthleteForm
            action={updateWithId}
            defaultName={athlete.name}
            defaultFormat={athlete.format}
            submitLabel="Guardar cambios"
          />
          <div className="mt-4">
            <DeleteButton
              action={deleteWithId}
              confirmMessage={`Borrar a ${athlete.name}? Esto tambien borra sus semanas.`}
            />
          </div>
        </div>

        <div>
          <h2 className="mb-3 font-heading text-lg font-bold text-neutral-50">Semanas</h2>
          {athlete.weeks.length === 0 ? (
            <p className="text-sm text-neutral-500">Sin semanas todavia.</p>
          ) : (
            <ul className="flex flex-col gap-2">
              {athlete.weeks.map((week) => (
                <li key={week.id}>
                  <Link
                    href={`/weeks/${week.id}`}
                    className="flex items-center justify-between rounded-lg border border-neutral-800 px-4 py-3 hover:border-neutral-700"
                  >
                    <div>
                      <p className="text-sm font-medium text-neutral-100">{week.semana}</p>
                      <p className="text-xs text-neutral-500">{FORMAT_LABEL[week.format]}</p>
                    </div>
                    <span className="text-xs text-neutral-500">
                      {WEEK_STATUS_LABEL[week.status]}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </>
  );
}
