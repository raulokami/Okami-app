import { AppHeader } from "@/components/app-header";
import { AthleteForm } from "@/components/athlete-form";
import { requireRole } from "@/lib/require-role";
import { createAthlete } from "@/app/athletes/actions";

export default async function NewAthletePage() {
  await requireRole(["OWNER", "COACH"]);

  return (
    <>
      <AppHeader />
      <main className="flex flex-col gap-6 px-6 py-10">
        <h1 className="font-heading text-2xl font-bold text-neutral-50">Nuevo atleta</h1>
        <div className="max-w-sm">
          <AthleteForm action={createAthlete} submitLabel="Crear atleta" />
        </div>
      </main>
    </>
  );
}
