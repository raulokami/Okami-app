import Link from "next/link";
import { auth } from "@clerk/nextjs/server";
import { prisma } from "@/lib/prisma";

export const dynamic = "force-dynamic";

async function getDbStatus() {
  try {
    await prisma.healthCheck.count();
    return { connected: true as const };
  } catch (error) {
    return { connected: false as const, message: (error as Error).message };
  }
}

export default async function Home() {
  const [db, { userId }] = await Promise.all([getDbStatus(), auth()]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8 px-6 py-16 text-center">
      <h1 className="font-heading text-4xl font-extrabold tracking-tight text-neutral-50 sm:text-5xl">
        OKAMI
      </h1>
      <p className="max-w-sm text-sm text-neutral-400 sm:text-base">
        Esqueleto de la plataforma. Fase 2: login real con Clerk (OWNER,
        COACH, ATLETA).
      </p>

      <Link
        href={userId ? "/dashboard" : "/sign-in"}
        className="rounded-lg bg-okami-accent px-6 py-3 text-sm font-semibold text-neutral-50 hover:bg-okami-accent/90 sm:text-base"
      >
        {userId ? "Ir al dashboard" : "Iniciar sesion"}
      </Link>

      <div
        className={`flex items-center gap-3 rounded-lg border px-4 py-3 text-sm sm:text-base ${
          db.connected
            ? "border-okami-accent/40 bg-okami-accent/10 text-neutral-100"
            : "border-red-900 bg-red-950/40 text-red-300"
        }`}
      >
        <span
          className={`h-2.5 w-2.5 shrink-0 rounded-full ${
            db.connected ? "bg-okami-accent" : "bg-red-500"
          }`}
        />
        {db.connected ? "Base de datos conectada" : "Sin conexion a la base de datos"}
      </div>
    </main>
  );
}
