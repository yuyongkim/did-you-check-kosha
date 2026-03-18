import { DisciplineWorkbench } from "@/components/workbench/discipline-workbench";
import { getDisciplineConfig } from "@/lib/mock-data";

export default function VesselPage() {
  return <DisciplineWorkbench config={getDisciplineConfig("vessel")} />;
}

