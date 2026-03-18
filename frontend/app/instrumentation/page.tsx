import { DisciplineWorkbench } from "@/components/workbench/discipline-workbench";
import { getDisciplineConfig } from "@/lib/mock-data";

export default function InstrumentationPage() {
  return <DisciplineWorkbench config={getDisciplineConfig("instrumentation")} />;
}

