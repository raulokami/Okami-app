import type { Appearance } from "@clerk/types";

export const clerkAppearance: Appearance = {
  variables: {
    colorBackground: "#1F1F1F",
    colorPrimary: "#C0392B",
    colorText: "#F5F5F5",
    colorTextSecondary: "#A3A3A3",
    colorInputBackground: "#141414",
    colorInputText: "#F5F5F5",
    colorNeutral: "#F5F5F5",
    colorDanger: "#C0392B",
    fontFamily: "var(--font-inter), sans-serif",
    borderRadius: "0.5rem",
  },
  elements: {
    card: "shadow-none border border-neutral-800",
    headerTitle: "font-heading",
    footerActionLink: "text-okami-accent hover:text-okami-accent/80",
  },
};
