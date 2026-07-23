"use client";

export function DeleteButton({
  action,
  confirmMessage,
  label = "Borrar",
}: {
  action: () => void;
  confirmMessage: string;
  label?: string;
}) {
  return (
    <form
      action={action}
      onSubmit={(event) => {
        if (!window.confirm(confirmMessage)) {
          event.preventDefault();
        }
      }}
    >
      <button
        type="submit"
        className="rounded-lg border border-red-900 bg-red-950/40 px-4 py-2 text-sm text-red-300 hover:bg-red-950/70"
      >
        {label}
      </button>
    </form>
  );
}
