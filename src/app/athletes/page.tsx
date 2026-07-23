import Link from "next/link";
import { AppHeader } from "@/components/app-header";
import { FORMAT_LABEL } from "@/lib/format-labels";
import { prisma } from "@/lib/prisma";
import { requireRole } from "@/lib/require-role";

export const dynamic = "force-dynamic";

export default async function AthletesPage() {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const athletes = await prisma.athlete.findMany({
    where: { organizationId: organization.id },
    orderBy: { createdAt: "desc" },
    include: { _count: { select: { weeks: true } } },
  });

  return (
    <>
      <AppHeader />
      <main className="flex flex-col gap-6 px-6 py-10">
        <div className="flex items-center justify-between">
          <h1 className="font-heading text-2xl font-bold text-neutral-50">Atletas</h1>
          <Link
            href="/athletes/new"
            className="rounded-lg bg-okami-accent px-4 py-2 text-sm font-semibold text-neutral-50 hover:bg-okami-accent/90"
          >
            Nuevo atleta
          </Link>
        </div>

        {athletes.length === 0 ? (
          <p className="text-sm text-neutral-500">Todavia no hay atletas.</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {athletes.map((athlete) => (
              <li key={athlete.id}>
                <Link
                  href={`/athletes/${athlete.id}`}
                  className="flex items-center justify-between rounded-lg border border-neutral-800 px-4 py-3 hover:border-neutral-700"
                >
                  <div>
                    <p className="text-sm font-medium text-neutral-100">{athlete.name}</p>
                    <p className="text-xs text-neutral-500">{FORMAT_LABEL[athlete.format]}</p>
                  </div>
                  <span className="text-xs text-neutral-500">
                    {athlete._count.weeks} semana{athlete._count.weeks === 1 ? "" : "s"}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </main>
    </>
  );
}
