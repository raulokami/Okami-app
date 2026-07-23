import Link from "next/link";
import { AppHeader } from "@/components/app-header";
import { FORMAT_LABEL, FORMAT_OPTIONS, WEEK_STATUS_LABEL } from "@/lib/format-labels";
import { prisma } from "@/lib/prisma";
import { requireRole } from "@/lib/require-role";
import type { Format, WeekStatus } from "@/generated/prisma/enums";

export const dynamic = "force-dynamic";

const STATUS_OPTIONS: [WeekStatus, string][] = [
  ["DRAFT", "Borrador"],
  ["GENERATED", "Generada"],
  ["SENT", "Enviada"],
];

export default async function WeeksPage({
  searchParams,
}: {
  searchParams: { format?: string; status?: string };
}) {
  const { organization } = await requireRole(["OWNER", "COACH"]);

  const format = searchParams.format as Format | undefined;
  const status = searchParams.status as WeekStatus | undefined;

  const weeks = await prisma.week.findMany({
    where: {
      organizationId: organization.id,
      ...(format ? { format } : {}),
      ...(status ? { status } : {}),
    },
    orderBy: { createdAt: "desc" },
    include: { athlete: { select: { name: true } } },
  });

  return (
    <>
      <AppHeader />
      <main className="flex flex-col gap-6 px-6 py-10">
        <div className="flex items-center justify-between">
          <h1 className="font-heading text-2xl font-bold text-neutral-50">Semanas</h1>
          <Link
            href="/generate"
            className="rounded-lg bg-okami-accent px-4 py-2 text-sm font-semibold text-neutral-50 hover:bg-okami-accent/90"
          >
            Nueva semana
          </Link>
        </div>

        <form method="get" className="flex flex-wrap gap-3">
          <select
            name="format"
            defaultValue={format ?? ""}
            className="rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 text-sm text-neutral-100"
          >
            <option value="">Todos los formatos</option>
            {FORMAT_OPTIONS.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
          <select
            name="status"
            defaultValue={status ?? ""}
            className="rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 text-sm text-neutral-100"
          >
            <option value="">Todos los estados</option>
            {STATUS_OPTIONS.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
          <button
            type="submit"
            className="rounded-lg border border-neutral-800 px-4 py-2 text-sm text-neutral-100 hover:border-neutral-700"
          >
            Filtrar
          </button>
        </form>

        {weeks.length === 0 ? (
          <p className="text-sm text-neutral-500">Sin semanas todavia.</p>
        ) : (
          <ul className="flex flex-col gap-2">
            {weeks.map((week) => (
              <li key={week.id}>
                <Link
                  href={`/weeks/${week.id}`}
                  className="flex items-center justify-between rounded-lg border border-neutral-800 px-4 py-3 hover:border-neutral-700"
                >
                  <div>
                    <p className="text-sm font-medium text-neutral-100">
                      {week.semana} &middot; {week.athlete?.name ?? "Clase"}
                    </p>
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
      </main>
    </>
  );
}
