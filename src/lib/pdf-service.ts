import "server-only";
import type { Format } from "@/generated/prisma/enums";

// pdf-service/parser.py es un parser unificado: cubre clase/atleta/hybrid/
// recomposicion/hybrid individual. Solo SISTEMA_INDIVIDUAL usa el parser
// dedicado (parser_individual.py). Ver pdf-service/README.md.
const INDIVIDUAL_FORMATS: Format[] = ["SISTEMA_INDIVIDUAL"];

function endpointFor(format: Format): "/pdf/general" | "/pdf/individual" {
  return INDIVIDUAL_FORMATS.includes(format) ? "/pdf/individual" : "/pdf/general";
}

export async function generateWeekPdf(
  format: Format,
  texto: string,
  filename: string,
): Promise<Uint8Array<ArrayBuffer>> {
  const baseUrl = process.env.PDF_SERVICE_URL;
  if (!baseUrl) {
    throw new Error("PDF_SERVICE_URL no esta configurada");
  }

  const apiKey = process.env.PDF_SERVICE_API_KEY;

  const response = await fetch(`${baseUrl}${endpointFor(format)}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(apiKey ? { "X-Api-Key": apiKey } : {}),
    },
    body: JSON.stringify({ texto, filename }),
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    throw new Error(detail?.detail ?? `pdf-service respondio ${response.status}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  return new Uint8Array(arrayBuffer);
}
