import type { Role } from "@/generated/prisma/enums";

// Los roles custom de Organization en Clerk (dashboard.clerk.com -> Organizations -> Roles)
// deben crearse con estos keys exactos para que el mapeo funcione.
const CLERK_ROLE_TO_PRISMA_ROLE: Record<string, Role> = {
  "org:owner": "OWNER",
  "org:coach": "COACH",
  "org:athlete": "ATHLETE",
  // Fallback a los roles por defecto de Clerk si aun no se crearon los custom.
  "org:admin": "OWNER",
  "org:member": "ATHLETE",
};

export function mapClerkRoleToPrismaRole(clerkOrgRole: string | null | undefined): Role {
  if (!clerkOrgRole) return "ATHLETE";
  return CLERK_ROLE_TO_PRISMA_ROLE[clerkOrgRole] ?? "ATHLETE";
}
