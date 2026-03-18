import { DisciplineWorkbench } from "@/components/workbench/discipline-workbench";
import { getDisciplineConfig } from "@/lib/mock-data";

export default function CivilPage() {
  return <DisciplineWorkbench config={getDisciplineConfig("civil")} />;
}

