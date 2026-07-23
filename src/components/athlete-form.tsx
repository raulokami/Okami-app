import { FORMAT_OPTIONS } from "@/lib/format-labels";

export function AthleteForm({
  action,
  defaultName,
  defaultFormat,
  submitLabel,
}: {
  action: (formData: FormData) => void;
  defaultName?: string;
  defaultFormat?: string;
  submitLabel: string;
}) {
  return (
    <form action={action} className="flex flex-col gap-4">
      <div className="flex flex-col gap-1">
        <label htmlFor="name" className="text-sm text-neutral-400">
          Nombre
        </label>
        <input
          id="name"
          name="name"
          type="text"
          required
          defaultValue={defaultName}
          className="rounded-lg border border-neutral-800 bg-neutral-900 px-3 py-2 text-sm text-neutral-100 outline-none focus:border-okami-accent"
        />
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

      <button
        type="submit"
        className="w-fit rounded-lg bg-okami-accent px-4 py-2 text-sm font-semibold text-neutral-50 hover:bg-okami-accent/90"
      >
        {submitLabel}
      </button>
    </form>
  );
}
