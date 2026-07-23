import { OrganizationList } from "@clerk/nextjs";

export default function OnboardingPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-10 px-6 py-16">
      <div className="max-w-sm text-center">
        <h1 className="font-heading text-2xl font-bold text-neutral-50">
          Falta un paso
        </h1>
        <p className="mt-2 text-sm text-neutral-400">
          Crea tu box (si eres OWNER) o acepta una invitacion pendiente (si
          eres COACH o ATLETA) para continuar.
        </p>
      </div>

      <OrganizationList
        hidePersonal
        afterSelectOrganizationUrl="/dashboard"
        afterCreateOrganizationUrl="/dashboard"
      />
    </main>
  );
}
