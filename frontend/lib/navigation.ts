import { Discipline } from "@/lib/types";

export const NAV_ITEMS: Array<{ discipline: Discipline; label: string; tag: string; href: string }> = [
  { discipline: "piping", label: "Piping", tag: "PIP", href: "/piping" },
  { discipline: "vessel", label: "Static Equipment", tag: "VES", href: "/vessel" },
  { discipline: "rotating", label: "Rotating", tag: "ROT", href: "/rotating" },
  { discipline: "electrical", label: "Electrical", tag: "ELE", href: "/electrical" },
  { discipline: "instrumentation", label: "Instrumentation", tag: "INS", href: "/instrumentation" },
  { discipline: "steel", label: "Steel Structure", tag: "STL", href: "/steel" },
  { discipline: "civil", label: "Civil Concrete", tag: "CIV", href: "/civil" },
];

