# Okami App

Fase 1 — scaffold: Next.js 14 (App Router) + Prisma + Postgres, con el
tema visual fijo de Okami (fondo `#1F1F1F`, acento `#C0392B`,
Montserrat/Inter, mobile-first, dark theme). Sin auth, pagos ni lógica de
negocio todavía.

## Stack

- Next.js 14 (App Router), TypeScript, Tailwind CSS
- Prisma ORM 7 (driver adapter `@prisma/adapter-pg`)
- Postgres (Railway en producción, local en desarrollo)

## Desarrollo local

1. Instala dependencias:

   ```bash
   npm install
   ```

2. Copia `.env.example` a `.env` y apunta `DATABASE_URL` a un Postgres
   local o a la instancia de Railway:

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

   Abre [http://localhost:3000](http://localhost:3000). La página muestra
   un indicador de "Base de datos conectada" que hace una consulta real
   contra Postgres en cada request (`GET /api/health` expone lo mismo como
   JSON).

## Deploy

### 1. Postgres en Railway

1. Crea un proyecto en [Railway](https://railway.app) y añade un plugin
   de **PostgreSQL**.
2. Copia la `DATABASE_URL` que Railway genera (pestaña *Connect*).

### 2. App en Vercel

1. Importa este repositorio en [Vercel](https://vercel.com/new).
2. En **Settings → Environment Variables**, añade `DATABASE_URL` con el
   valor de Railway (para los entornos Production y Preview).
3. Despliega. El script `build` corre `prisma migrate deploy` antes de
   `next build`, así que las migraciones se aplican automáticamente en
   cada deploy.

No hace falta configuración adicional (`vercel.json`, etc.) — Vercel
detecta Next.js automáticamente.

## Estructura

```
prisma/schema.prisma   Modelo de datos (Fase 1: solo HealthCheck)
src/lib/prisma.ts       Cliente Prisma singleton (driver adapter pg)
src/app/layout.tsx      Layout base, tema dark fijo, fuentes Montserrat/Inter
src/app/page.tsx        Home con verificación de conexión a la DB
src/app/api/health/     Endpoint de health check
```
