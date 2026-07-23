import "server-only";
import { auth, clerkClient } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";
import { mapClerkRoleToPrismaRole } from "@/lib/roles";

/**
 * Sincroniza la Organization y el User de Clerk hacia Prisma en cada
 * request autenticado. Sustituye (por ahora) al webhook de Clerk, que
 * solo se puede verificar una vez la app tenga una URL publica: ver
 * /api/webhooks/clerk para el mismo mapeo aplicado ahi para produccion.
 */
export async function syncCurrentUser() {
  const { userId, orgId, orgRole } = await auth();

  if (!userId || !orgId) {
    return null;
  }

  const client = await clerkClient();
  const [clerkUser, clerkOrg] = await Promise.all([
    client.users.getUser(userId),
    client.organizations.getOrganization({ organizationId: orgId }),
  ]);

  const email = clerkUser.primaryEmailAddress?.emailAddress ?? clerkUser.emailAddresses[0]?.emailAddress;

  if (!email) {
    throw new Error(`Clerk user ${userId} has no email address`);
  }

  const organization = await prisma.organization.upsert({
    where: { id: orgId },
    create: { id: orgId, name: clerkOrg.name },
    update: { name: clerkOrg.name },
  });

  const user = await prisma.user.upsert({
    where: { id: userId },
    create: {
      id: userId,
      organizationId: organization.id,
      email,
      role: mapClerkRoleToPrismaRole(orgRole),
    },
    update: {
      organizationId: organization.id,
      email,
      role: mapClerkRoleToPrismaRole(orgRole),
    },
  });

  return { organization, user };
}
