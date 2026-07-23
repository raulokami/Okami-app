# Okami PDF Service (Fase 4)

Microservicio Python que envuelve los parsers/generadores de PDF existentes
(`parser.py`, `generar_pdf.py`, `parser_individual.py`,
`generar_pdf_individual.py`) con una capa HTTP (FastAPI). La lógica de
parseo y de generación de PDF no se ha tocado — `main.py` solo importa y
llama a `generar_pdf` / `generar_pdf_individual` tal cual estaban.

Requiere el binario `wkhtmltopdf` instalado en el sistema (lo instala el
`Dockerfile`); en local: `apt-get install wkhtmltopdf` / `brew install
wkhtmltopdf`.

## Desarrollo local

```bash
cd pdf-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Endpoints

- `GET /health` — health check.
- `POST /pdf/general` — envuelve `generar_pdf()`. `parser.py` es un
  parser unificado: cubre `CLASE_METCON`/`CLASE_ENDURANCE`/`ATLETA`/
  `HYBRID`/`RECOMPOSICION` **y también hybrid individual** (mismos
  marcadores `FORMATO:`/`TIPO_DIA:` que distinguen días Box/Run/etc.) —
  no hace falta un endpoint aparte para hybrid individual.
- `POST /pdf/individual` — envuelve `generar_pdf_individual()` (formato
  `SISTEMA_INDIVIDUAL`).

Body en ambos casos:

```json
{ "texto": "FORMATO: ...\n...", "filename": "opcional.pdf" }
```

Respuesta: el PDF binario (`application/pdf`). Si el texto no trae
ningún día/sesión reconocible, responde `422` con el mensaje de error del
parser original.

### Autenticación

Si se define la variable de entorno `PDF_SERVICE_API_KEY`, todas las
rutas de generación exigen el header `X-Api-Key` con ese valor (401 si
falta o no coincide). Sin la variable definida, el servicio queda abierto
— pensado solo para desarrollo local.

## Deploy en Railway

1. En [railway.app](https://railway.app), **New Project → Deploy from
   GitHub repo** → selecciona `raulokami/Okami-app`.
2. En el servicio creado, **Settings → Root Directory** → pon
   `pdf-service`. Railway detecta el `Dockerfile` y `railway.json` de esa
   carpeta automáticamente (build Docker, healthcheck en `/health`).
3. **Settings → Networking → Generate Domain** para obtener una URL
   pública tipo `https://<servicio>.up.railway.app`.
4. (Opcional pero recomendado) **Variables** → añade `PDF_SERVICE_API_KEY`
   con un valor aleatorio propio (p. ej. generado con
   `openssl rand -hex 32`) para que el servicio no quede abierto a
   cualquiera que tenga la URL.
5. Espera al deploy (el build instala `wkhtmltopdf` vía `apt-get`, tarda
   1-2 min) y confirma que `https://<servicio>.up.railway.app/health`
   responde `{"status":"ok"}`.
6. En el proyecto de Vercel del Next.js (`Settings → Environment
   Variables`), añade:
   - `PDF_SERVICE_URL` = la URL del paso 3 (sin barra final).
   - `PDF_SERVICE_API_KEY` = el mismo valor del paso 4, si lo configuraste.

   Redeploy del Next.js para que recoja las variables nuevas.

## Pendiente

- Nada bloqueante — con el deploy en Railway y las env vars en Vercel, el
  flujo `/weeks/[id]` → Generar PDF queda operativo de punta a punta.
