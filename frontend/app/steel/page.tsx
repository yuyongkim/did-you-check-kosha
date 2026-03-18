import { DisciplineWorkbench } from "@/components/workbench/discipline-workbench";
import { getDisciplineConfig } from "@/lib/mock-data";

export default function SteelPage() {
  return <DisciplineWorkbench config={getDisciplineConfig("steel")} />;
}

