import { OrganizationProfile } from "@clerk/nextjs";
import { AppHeader } from "@/components/app-header";
import { requireRole } from "@/lib/require-role";

export const dynamic = "force-dynamic";

export default async function OrganizationPage() {
  await requireRole(["OWNER"]);

  return (
    <>
      <AppHeader />
      <main className="flex flex-col items-center px-6 py-10">
        <OrganizationProfile />
      </main>
    </>
  );
}
