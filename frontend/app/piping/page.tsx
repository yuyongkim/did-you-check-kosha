import { DisciplineWorkbench } from "@/components/workbench/discipline-workbench";
import { getDisciplineConfig } from "@/lib/mock-data";

export default function PipingPage() {
  return <DisciplineWorkbench config={getDisciplineConfig("piping")} />;
}

