import type { Format, WeekStatus } from "@/generated/prisma/enums";

export const FORMAT_LABEL: Record<Format, string> = {
  CLASE_METCON: "Clase Metcon",
  CLASE_ENDURANCE: "Clase Endurance",
  ATLETA: "Atleta",
  HYBRID: "Hybrid",
  RECOMPOSICION: "Recomposicion",
  SISTEMA_INDIVIDUAL: "Sistema Individual",
  HYROX_INDIVIDUAL: "HYROX Individual",
};

export const FORMAT_OPTIONS = Object.entries(FORMAT_LABEL) as [Format, string][];

export const WEEK_STATUS_LABEL: Record<WeekStatus, string> = {
  DRAFT: "Borrador",
  GENERATED: "Generada",
  SENT: "Enviada",
};
