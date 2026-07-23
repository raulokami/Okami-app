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
- `POST /pdf/general` — envuelve `generar_pdf()` (formatos
  `CLASE_METCON`/`CLASE_ENDURANCE`/`ATLETA`/`HYBRID`/`RECOMPOSICION`, los
  que trae el marcador `FORMATO:` del texto que parsea `parser.py`).
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

## Pendiente

- `POST /pdf/hybrid-individual`, en cuanto se suban `parser_hybrid_individual.py`
  y su `generar_pdf_hybrid_individual.py` correspondientes.
- Conectar el resultado (`pdfUrl`) con `Week` desde el Next.js (fuera del
  alcance de esta capa HTTP).
