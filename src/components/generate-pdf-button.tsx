"use client";

import { useFormStatus } from "react-dom";

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button
      type="submit"
      disabled={pending}
      className="w-fit rounded-lg border border-neutral-800 px-4 py-2 text-sm text-neutral-100 hover:border-neutral-700 disabled:cursor-not-allowed disabled:opacity-60"
    >
      {pending ? "Generando PDF..." : "Generar PDF"}
    </button>
  );
}

export function GeneratePdfButton({ action }: { action: () => void }) {
  return (
    <form action={action}>
      <SubmitButton />
    </form>
  );
}
