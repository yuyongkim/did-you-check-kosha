export type GlossaryDiscipline =
  | "all"
  | "common"
  | "piping"
  | "vessel"
  | "rotating"
  | "electrical"
  | "instrumentation"
  | "steel"
  | "civil";

export const GLOSSARY_DISCIPLINE_FILTERS: Array<{ value: GlossaryDiscipline; label: string }> = [
  { value: "all", label: "All" },
  { value: "common", label: "Common" },
  { value: "piping", label: "Piping" },
  { value: "vessel", label: "Vessel" },
  { value: "rotating", label: "Rotating" },
  { value: "electrical", label: "Electrical" },
  { value: "instrumentation", label: "Instrumentation" },
  { value: "steel", label: "Steel" },
  { value: "civil", label: "Civil" },
];
