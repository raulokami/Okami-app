import os
import re
import subprocess
import tempfile
from typing import Callable

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from generar_pdf import generar_pdf
from generar_pdf_individual import generar_pdf_individual

API_KEY = os.environ.get("PDF_SERVICE_API_KEY")

app = FastAPI(title="Okami PDF Service")


class GenerateRequest(BaseModel):
    texto: str
    filename: str | None = None


def check_api_key(x_api_key: str | None) -> None:
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida o ausente")


def safe_filename(name: str | None, default: str) -> str:
    name = re.sub(r'[\r\n"]', "", name or default).strip()
    return name or default


def run_generator(generar_fn: Callable[[str, str], dict], payload: GenerateRequest, default_filename: str) -> Response:
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_path = os.path.join(tmp_dir, "output.pdf")
        try:
            generar_fn(payload.texto, output_path)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except subprocess.CalledProcessError as exc:
            raise HTTPException(status_code=500, detail="Error generando el PDF (wkhtmltopdf)") from exc

        with open(output_path, "rb") as f:
            pdf_bytes = f.read()

    filename = safe_filename(payload.filename, default_filename)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/pdf/general")
def pdf_general(payload: GenerateRequest, x_api_key: str | None = Header(default=None)) -> Response:
    check_api_key(x_api_key)
    return run_generator(generar_pdf, payload, "okami.pdf")


@app.post("/pdf/individual")
def pdf_individual(payload: GenerateRequest, x_api_key: str | None = Header(default=None)) -> Response:
    check_api_key(x_api_key)
    return run_generator(generar_pdf_individual, payload, "okami-individual.pdf")
