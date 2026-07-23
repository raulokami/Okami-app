import { FORMAT_OPTIONS } from "@/lib/format-labels";

export function WeekForm({
  action,
  athletes,
  defaultAthleteId,
  defaultFormat,
  defaultSubformato,
  defaultSemana,
  defaultRawText,
  submitLabel,
}: {
  action: (formData: FormData) => void;
  athletes: { id: string; name: string }[];
  defaultAthleteId?: string | null;
  defaultFormat?: string;
  defaultSubformato?: string | null;
  defaultSemana?: string;
  defaultRawText?: string;
  submitLabel: string;
}) {
  return (
    <form action={action} className="flex flex-col gap-4">
      <div className="flex flex-col gap-1">
        <label htmlFor="athleteId" className="text-sm text-neutral-400">
          Atleta (opcional, dejar en blanco para una clase)
        </label>
        <select
          id="athleteId"
          name="athleteId"
          defaultValue={defaultAthleteId ?? ""}
          className="rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 text-sm text-neutral-100 outline-none focus:border-okami-accent"
        >
          <option value="">— Sin atleta (clase) —</option>
          {athletes.map((athlete) => (
            <option key={athlete.id} value={athlete.id}>
              {athlete.name}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="format" className="text-sm text-neutral-400">
          Formato
        </label>
        <select
          id="format"
          name="format"
          required
          defaultValue={defaultFormat}
          className="rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 text-sm text-neutral-100 outline-none focus:border-okami-accent"
        >
          {FORMAT_OPTIONS.map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="subformato" className="text-sm text-neutral-400">
          Subformato (opcional)
        </label>
        <input
          id="subformato"
          name="subformato"
          type="text"
          defaultValue={defaultSubformato ?? ""}
          className="rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 text-sm text-neutral-100 outline-none focus:border-okami-accent"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="semana" className="text-sm text-neutral-400">
          Semana
        </label>
        <input
          id="semana"
          name="semana"
          type="text"
          required
          placeholder="Semana 12"
          defaultValue={defaultSemana}
          className="rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 text-sm text-neutral-100 outline-none focus:border-okami-accent"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="rawText" className="text-sm text-neutral-400">
          Texto de la programacion
        </label>
        <textarea
          id="rawText"
          name="rawText"
          required
          rows={12}
          defaultValue={defaultRawText}
          className="rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 font-mono text-sm text-neutral-100 outline-none focus:border-okami-accent"
        />
      </div>

      <button
        type="submit"
        className="w-fit rounded-lg bg-okami-accent px-4 py-2 text-sm font-semibold text-neutral-50 hover:bg-okami-accent/90"
      >
        {submitLabel}
      </button>
    </form>
  );
}
