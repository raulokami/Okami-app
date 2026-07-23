import "server-only";
import { notFound } from "next/navigation";
import type { Role } from "@/generated/prisma/enums";
import { syncCurrentUser } from "@/lib/sync-user";

export async function requireRole(allowed: Role[]) {
  const synced = await syncCurrentUser();

  if (!synced || !allowed.includes(synced.user.role)) {
    notFound();
  }

  return synced;
}
