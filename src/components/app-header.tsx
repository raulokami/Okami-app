import Link from "next/link";
import { OrganizationSwitcher, UserButton } from "@clerk/nextjs";

export function AppHeader() {
  return (
    <header className="flex items-center justify-between border-b border-neutral-800 px-6 py-4">
      <Link href="/dashboard" className="font-heading text-lg font-bold text-neutral-50">
        OKAMI
      </Link>
      <div className="flex items-center gap-4">
        <OrganizationSwitcher hidePersonal afterSelectOrganizationUrl="/dashboard" />
        <UserButton />
      </div>
    </header>
  );
}
