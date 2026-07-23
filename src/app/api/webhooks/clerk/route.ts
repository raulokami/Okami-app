import { headers } from "next/headers";
import { NextResponse } from "next/server";
import { Webhook } from "svix";
import type { WebhookEvent } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";
import { mapClerkRoleToPrismaRole } from "@/lib/roles";

export const dynamic = "force-dynamic";

async function verifyRequest(req: Request): Promise<WebhookEvent> {
  const webhookSecret = process.env.CLERK_WEBHOOK_SECRET;
  if (!webhookSecret) {
    throw new Error("CLERK_WEBHOOK_SECRET is not set");
  }

  const headerPayload = await headers();
  const svixId = headerPayload.get("svix-id");
  const svixTimestamp = headerPayload.get("svix-timestamp");
  const svixSignature = headerPayload.get("svix-signature");

  if (!svixId || !svixTimestamp || !svixSignature) {
    throw new Error("Missing svix headers");
  }

  const body = await req.text();
  const wh = new Webhook(webhookSecret);

  return wh.verify(body, {
    "svix-id": svixId,
    "svix-timestamp": svixTimestamp,
    "svix-signature": svixSignature,
  }) as WebhookEvent;
}

// Sincronizacion de respaldo para produccion: mantiene Organization/User al
// dia aunque nadie visite la app (p.ej. si se borra una organizacion o
// membresia en Clerk). El camino principal en desarrollo es
// src/lib/sync-user.ts, que sincroniza en cada request autenticado.
export async function POST(req: Request) {
  let event: WebhookEvent;
  try {
    event = await verifyRequest(req);
  } catch (error) {
    return NextResponse.json(
      { error: (error as Error).message },
      { status: 400 },
    );
  }

  switch (event.type) {
    case "organization.created":
    case "organization.updated": {
      const org = event.data;
      await prisma.organization.upsert({
        where: { id: org.id },
        create: { id: org.id, name: org.name },
        update: { name: org.name },
      });
      break;
    }

    case "organization.deleted": {
      if (event.data.id) {
        await prisma.organization.deleteMany({ where: { id: event.data.id } });
      }
      break;
    }

    case "organizationMembership.created":
    case "organizationMembership.updated": {
      const membership = event.data;
      const clerkUser = membership.public_user_data;
      const email = clerkUser?.identifier;

      if (clerkUser?.user_id && email) {
        await prisma.user.upsert({
          where: { id: clerkUser.user_id },
          create: {
            id: clerkUser.user_id,
            organizationId: membership.organization.id,
            email,
            role: mapClerkRoleToPrismaRole(membership.role),
          },
          update: {
            organizationId: membership.organization.id,
            email,
            role: mapClerkRoleToPrismaRole(membership.role),
          },
        });
      }
      break;
    }

    case "organizationMembership.deleted": {
      const userId = event.data.public_user_data?.user_id;
      if (userId) {
        await prisma.user.deleteMany({ where: { id: userId } });
      }
      break;
    }

    default:
      break;
  }

  return NextResponse.json({ received: true });
}
