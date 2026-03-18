import { DisciplineWorkbench } from "@/components/workbench/discipline-workbench";
import { getDisciplineConfig } from "@/lib/mock-data";

export default function RotatingPage() {
  return <DisciplineWorkbench config={getDisciplineConfig("rotating")} />;
}

