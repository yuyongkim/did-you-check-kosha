import type { GlossaryDiscipline } from "@/lib/glossary-types";

export interface StandardGlossaryEntry {
  code: string;
  label: string;
  summary: string;
  publisher: "ASME" | "API" | "ISO" | "IEEE" | "IEC" | "AISC" | "ACI";
  officialUrl: string;
  accessNote: string;
  disciplines: GlossaryDiscipline[];
}

export interface StandardDeepGuidance {
  engineeringIntent: string;
  practicalUse: string;
  whatToVerify: string[];
  commonMisses: string[];
}
