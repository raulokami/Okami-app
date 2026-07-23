# Okami App

Fase 1 (scaffold) + Fase 2 (auth) + Fase 3 (CRUD Athletes/Weeks) + Fase 4
(generación real de PDF vía microservicio Python): Next.js 14 (App
Router) + Prisma + Postgres + Clerk (login real, 3 roles: OWNER, COACH,
ATLETA). Tema visual fijo de Okami (fondo `#1F1F1F`, acento `#C0392B`,
Montserrat/Inter, mobile-first, dark theme). Todavía sin pagos (Fase 6).

## Stack

- Next.js 14 (App Router), TypeScript, Tailwind CSS
- Prisma ORM 7 (driver adapter `@prisma/adapter-pg`)
- Postgres (Railway en producción, local en desarrollo)
- Clerk (auth + Organizations para multi-tenant por box)

## Desarrollo local

1. Instala dependencias:

   ```bash
   npm install
   ```

2. Copia `.env.example` a `.env` y rellena:
   - `DATABASE_URL`: Postgres local o de Railway.
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` / `CLERK_SECRET_KEY`: de tu app en
     [dashboard.clerk.com](https://dashboard.clerk.com) → **API Keys**.

   ```bash
   cp .env.example .env
   ```

3. Aplica las migraciones:

   ```bash
   npx prisma migrate dev
   ```

4. Arranca el servidor de desarrollo:

   ```bash
   npm run dev
   ```

   Abre [http://localhost:3000](http://localhost:3000).

## Configuración de Clerk (Fase 2)

1. **Organizations**: actívalo en el dashboard de tu app (menú
   **Organizations** → *Enable organizations*). Cada Organization = un box.
2. **Roles custom**: en **Organizations → Roles**, crea dos roles
   adicionales con estos keys exactos (Clerk ya trae `org:admin` y
   `org:member` por defecto):
   - `org:owner`
   - `org:coach`
   - `org:athlete`

   El mapeo a `enum Role` de Prisma está en `src/lib/roles.ts`. Si un
   miembro tiene el rol por defecto `org:admin` (p.ej. quien crea la
   organización desde `/onboarding`), se trata como `OWNER`; `org:member`
   se trata como `ATHLETE`.
3. **Invitar miembros con rol**: el OWNER puede invitar COACH/ATLETA desde
   `/organization` (usa el componente `<OrganizationProfile />` de Clerk),
   asignando el rol custom correspondiente en la invitación.
4. **Webhook (opcional, recomendado en producción)**: una vez desplegada
   la app, en **Webhooks** añade un endpoint a
   `https://tu-dominio/api/webhooks/clerk`, suscrito a
   `organization.created`, `organization.updated`, `organization.deleted`,
   `organizationMembership.created`, `organizationMembership.updated`,
   `organizationMembership.deleted`. Copia el *Signing Secret* a
   `CLERK_WEBHOOK_SECRET`.

   Sin el webhook, la sincronización Clerk → Prisma igual funciona vía
   `src/lib/sync-user.ts`, que hace upsert de `Organization`/`User` en cada
   request autenticado (`/dashboard`, `/organization`). El webhook es una
   capa extra para mantener los datos al día aunque nadie entre a la app
   (p.ej. si se borra una organización o membresía directamente en Clerk).

## Flujo de auth

- `/sign-in`, `/sign-up`: páginas de Clerk tematizadas.
- `/onboarding`: para usuarios autenticados sin organización — crear un
  box nuevo (OWNER) o aceptar una invitación pendiente (COACH/ATLETA).
- `/dashboard`: protegido por `middleware.ts`, requiere sesión + org
  activa. Muestra el rol real sincronizado desde Prisma.
- `/organization`: solo OWNER (gate por rol vía `requireRole`), gestión de
  miembros con `<OrganizationProfile />`.

## CRUD de atletas y semanas (Fase 3)

Todas las páginas están protegidas por rol (`OWNER`/`COACH`, vía
`requireRole`) y escopeadas a la `Organization` del usuario — las server
actions vuelven a validar rol y `organizationId` en cada mutación, no solo
en la página.

- `/athletes`: listado, alta (`/athletes/new`) y detalle/edición/borrado
  (`/athletes/[id]`) de atletas (nombre, formato).
- `/generate`: pega el texto de una programación y la guarda como `Week`
  en estado `DRAFT` (atleta opcional — en blanco para una clase).
- `/weeks`: histórico de semanas con filtro por formato/estado; cada una
  se puede editar o borrar desde `/weeks/[id]`, donde también está el
  botón **Generar PDF**.

## Generación de PDF (Fase 4)

`pdf-service/` es un microservicio Python (FastAPI) independiente del
Next.js — envuelve con una capa HTTP los parsers/generadores de PDF
existentes (`parser.py` + `generar_pdf.py`, parser unificado para
clase/atleta/hybrid/recomposición/hybrid individual, `parser_individual.py`
+ `generar_pdf_individual.py` para sistema individual; sin reescribir su
lógica). Detalles de endpoints, auth y despliegue en
[`pdf-service/README.md`](pdf-service/README.md).

Desde `/weeks/[id]`, el botón **Generar PDF** llama a la server action
`generatePdf` (`src/app/weeks/actions.ts`), que:

1. Llama a `PDF_SERVICE_URL` (`/pdf/general` o `/pdf/individual` segun el
   `Format` de la semana — mapeo en `src/lib/pdf-service.ts`).
2. Guarda los bytes del PDF en `WeekPdf` (tabla separada de `Week`, un
   solo registro por semana vía upsert — regenerar no acumula versiones,
   y se borra en cascada si se borra la `Week`).
3. Actualiza `Week.pdfUrl` a `/api/weeks/[id]/pdf` (ruta interna que sirve
   los bytes desde Postgres, protegida por rol/organización) y pasa
   `status` a `GENERATED`.

Variables de entorno nuevas (`.env.example`): `PDF_SERVICE_URL` (URL base
del microservicio) y `PDF_SERVICE_API_KEY` (opcional, debe coincidir con
la del `pdf-service` si este la exige).

## Deploy

### 1. Postgres en Railway

1. Crea un proyecto en [Railway](https://railway.app) y añade un plugin
   de **PostgreSQL**.
2. Copia la `DATABASE_URL` que Railway genera (pestaña *Connect*).

### 2. App en Vercel

1. Importa este repositorio en [Vercel](https://vercel.com/new).
2. En **Settings → Environment Variables**, añade `DATABASE_URL`,
   `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`, (tras
   configurar el webhook) `CLERK_WEBHOOK_SECRET`, y `PDF_SERVICE_URL` /
   `PDF_SERVICE_API_KEY` (URL pública donde esté desplegado `pdf-service/`),
   para Production y Preview.
3. Despliega. El script `build` corre `prisma migrate deploy` antes de
   `next build`, así que las migraciones se aplican automáticamente en
   cada deploy.

No hace falta configuración adicional (`vercel.json`, etc.) — Vercel
detecta Next.js automáticamente.

## Estructura

```
prisma/schema.prisma         Modelo de datos (HealthCheck, Organization, User, Athlete, Week, WeekPdf, Role, Format, WeekStatus)
src/middleware.ts             Proteccion de rutas por sesion/organizacion (Clerk)
src/lib/prisma.ts             Cliente Prisma singleton (driver adapter pg)
src/lib/sync-user.ts          Sync Clerk -> Prisma en cada request autenticado
src/lib/roles.ts              Mapeo rol de Clerk (org:*) -> enum Role de Prisma
src/lib/require-role.ts       Helper de gating por rol para paginas server
src/lib/format-labels.ts       Labels ES para Format/WeekStatus
src/lib/pdf-service.ts         Cliente HTTP del microservicio pdf-service (Fase 4)
src/components/               AppHeader, AthleteForm, WeekForm, DeleteButton, GeneratePdfButton
src/app/layout.tsx            Layout base, ClerkProvider tematizado, fuentes
src/app/page.tsx              Home publica (estado DB + link a login/dashboard)
src/app/sign-in/              Pagina de login (Clerk)
src/app/sign-up/              Pagina de registro (Clerk)
src/app/onboarding/           Crear/unirse a organizacion
src/app/dashboard/             Dashboard protegido, contadores y accesos por rol
src/app/organization/         Gestion de organizacion (solo OWNER)
src/app/athletes/             CRUD de atletas (OWNER/COACH)
src/app/generate/             Crear semana (guardado real)
src/app/weeks/                Historico de semanas, editar/borrar/generar PDF
src/app/api/health/           Endpoint de health check
src/app/api/webhooks/clerk/   Webhook de Clerk (sync de respaldo en produccion)
src/app/api/weeks/[id]/pdf/   Sirve los bytes del PDF generado (WeekPdf)
pdf-service/                  Microservicio Python (FastAPI) de generacion de PDF (Fase 4)
```
