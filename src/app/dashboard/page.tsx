import Link from "next/link";
import { redirect } from "next/navigation";
import { AppHeader } from "@/components/app-header";
import { prisma } from "@/lib/prisma";
import { syncCurrentUser } from "@/lib/sync-user";

export const dynamic = "force-dynamic";

const ROLE_LABEL: Record<string, string> = {
  OWNER: "Owner",
  COACH: "Coach",
  ATHLETE: "Atleta",
};

export default async function DashboardPage() {
  const synced = await syncCurrentUser();

  if (!synced) {
    redirect("/onboarding");
  }

  const { organization, user } = synced;
  const isStaff = user.role === "OWNER" || user.role === "COACH";

  const [athleteCount, draftWeekCount] = isStaff
    ? await Promise.all([
        prisma.athlete.count({ where: { organizationId: organization.id } }),
        prisma.week.count({
          where: { organizationId: organization.id, status: "DRAFT" },
        }),
      ])
    : [0, 0];

  return (
    <>
      <AppHeader />
      <main className="flex flex-col gap-6 px-6 py-10">
        <div>
          <h1 className="font-heading text-2xl font-bold text-neutral-50">
            Bienvenido, {ROLE_LABEL[user.role]}
          </h1>
          <p className="mt-1 text-sm text-neutral-400">
            {organization.name} &middot; {user.email}
          </p>
        </div>

        {isStaff && (
          <div className="flex flex-wrap gap-4">
            <Link
              href="/athletes"
              className="rounded-lg border border-neutral-800 px-4 py-3 text-sm text-neutral-100 hover:border-neutral-700"
            >
              Atletas
              <span className="ml-2 text-neutral-500">{athleteCount}</span>
            </Link>
            <Link
              href="/weeks"
              className="rounded-lg border border-neutral-800 px-4 py-3 text-sm text-neutral-100 hover:border-neutral-700"
            >
              Semanas en borrador
              <span className="ml-2 text-neutral-500">{draftWeekCount}</span>
            </Link>
            <Link
              href="/generate"
              className="rounded-lg bg-okami-accent px-4 py-3 text-sm font-semibold text-neutral-50 hover:bg-okami-accent/90"
            >
              Generar semana
            </Link>
          </div>
        )}

        {user.role === "OWNER" && (
          <Link
            href="/organization"
            className="w-fit rounded-lg border border-okami-accent/40 bg-okami-accent/10 px-4 py-2 text-sm text-neutral-100 hover:bg-okami-accent/20"
          >
            Gestionar organizacion y miembros
          </Link>
        )}

        <p className="text-sm text-neutral-500">
          Fase 3: CRUD de atletas y semanas, sin pagos ni PDF real todavia.
        </p>
      </main>
    </>
  );
}
