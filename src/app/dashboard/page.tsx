import Link from "next/link";
import { redirect } from "next/navigation";
import { AppHeader } from "@/components/app-header";
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

        {user.role === "OWNER" && (
          <Link
            href="/organization"
            className="w-fit rounded-lg border border-okami-accent/40 bg-okami-accent/10 px-4 py-2 text-sm text-neutral-100 hover:bg-okami-accent/20"
          >
            Gestionar organizacion y miembros
          </Link>
        )}

        <p className="text-sm text-neutral-500">
          Fase 2: login real con Clerk, sin logica de negocio todavia.
        </p>
      </main>
    </>
  );
}
