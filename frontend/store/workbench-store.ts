import { create } from "zustand";

import { ApiMode, CalculationResponse, Discipline, RunHistoryEntry } from "@/lib/types";

export type WorkbenchMode = "beginner" | "standard" | "master";

const MAX_HISTORY = 100;

const envApiMode = (process.env.NEXT_PUBLIC_API_MODE ?? "").trim().toLowerCase();
const hasBackendPrefix = Boolean((process.env.NEXT_PUBLIC_BACKEND_API_PREFIX ?? "").trim());
const defaultApiMode: ApiMode =
  envApiMode === "backend" || (envApiMode !== "mock" && hasBackendPrefix) ? "backend" : "mock";

interface WorkbenchStore {
  activeDiscipline: Discipline;
  activeProjectId: string;
  activeAssetId: string;
  apiMode: ApiMode;
  backendApiPrefix: string;
  workbenchMode: WorkbenchMode;
  resultByDiscipline: Partial<Record<Discipline, CalculationResponse>>;
  runHistory: RunHistoryEntry[];
  setActiveDiscipline: (discipline: Discipline) => void;
  setProject: (projectId: string) => void;
  setAsset: (assetId: string) => void;
  setApiMode: (mode: ApiMode) => void;
  setBackendApiPrefix: (prefix: string) => void;
  setWorkbenchMode: (mode: WorkbenchMode) => void;
  setResult: (discipline: Discipline, result: CalculationResponse) => void;
  appendRunHistory: (entry: RunHistoryEntry) => void;
  clearRunHistory: () => void;
  clearRunHistoryByDiscipline: (discipline: Discipline) => void;
}

export const useWorkbenchStore = create<WorkbenchStore>((set) => ({
  activeDiscipline: "piping",
  activeProjectId: "PROJECT-ALPHA",
  activeAssetId: "ASSET-001",
  apiMode: defaultApiMode,
  backendApiPrefix: process.env.NEXT_PUBLIC_BACKEND_API_PREFIX ?? "",
  workbenchMode: "standard",
  resultByDiscipline: {},
  runHistory: [],
  setActiveDiscipline: (discipline) => set({ activeDiscipline: discipline }),
  setProject: (projectId) => set({ activeProjectId: projectId }),
  setAsset: (assetId) => set({ activeAssetId: assetId }),
  setApiMode: (mode) => set({ apiMode: mode }),
  setBackendApiPrefix: (prefix) => set({ backendApiPrefix: prefix }),
  setWorkbenchMode: (mode) => set({ workbenchMode: mode }),
  setResult: (discipline, result) =>
    set((state) => ({
      resultByDiscipline: {
        ...state.resultByDiscipline,
        [discipline]: result,
      },
    })),
  appendRunHistory: (entry) =>
    set((state) => ({
      runHistory: [entry, ...state.runHistory].slice(0, MAX_HISTORY),
    })),
  clearRunHistory: () => set({ runHistory: [] }),
  clearRunHistoryByDiscipline: (discipline) =>
    set((state) => ({
      runHistory: state.runHistory.filter((entry) => entry.discipline !== discipline),
    })),
}));
