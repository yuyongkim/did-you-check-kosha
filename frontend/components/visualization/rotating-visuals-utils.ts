import {
  DRIVER_LABELS,
  MACHINE_LABELS,
  type LocalizedLabel,
  type UiLanguage,
} from "@/components/visualization/rotating-visuals-content";

export function indexVariant(value: number): "ok" | "warning" | "blocked" {
  if (value >= 7) return "ok";
  if (value >= 4) return "warning";
  return "blocked";
}

export function spectrumData(language: UiLanguage, vibration: number) {
  return [
    { band: "1X", amp: vibration, fault: language === "ko" ? "언밸런스" : "Unbalance" },
    { band: "2X", amp: vibration * 0.52, fault: language === "ko" ? "미스얼라인먼트" : "Misalignment" },
    { band: "BPFO", amp: vibration * 0.36, fault: language === "ko" ? "베어링 외륜" : "Bearing outer race" },
    { band: "BPFI", amp: vibration * 0.31, fault: language === "ko" ? "베어링 내륜" : "Bearing inner race" },
  ];
}

export function processMode(machineType: string): "steam" | "compressor" | "pump" | "generic" {
  if (machineType === "steam_turbine") return "steam";
  if (
    machineType === "compressor"
    || machineType === "centrifugal_compressor"
    || machineType === "axial_compressor"
    || machineType === "screw_compressor"
    || machineType === "recip_compressor"
    || machineType === "expander"
  ) {
    return "compressor";
  }
  if (machineType === "pump" || machineType === "recip_pump") return "pump";
  return "generic";
}

function localizedLabel(
  language: UiLanguage,
  source: Record<string, LocalizedLabel>,
  value: string,
  fallback: LocalizedLabel,
): string {
  const label = source[value] ?? fallback;
  return language === "ko" ? label.ko : label.en;
}

export function machineLabel(language: UiLanguage, machineType: string): string {
  return localizedLabel(language, MACHINE_LABELS, machineType, {
    ko: "회전기기",
    en: "Rotating Machine",
  });
}

export function driverLabel(language: UiLanguage, driverType: string): string {
  return localizedLabel(language, DRIVER_LABELS, driverType, {
    ko: "구동기",
    en: "Driver",
  });
}

export function enumLabel(
  language: UiLanguage,
  value: string,
  dictionary: Record<string, LocalizedLabel>,
): string {
  const item = dictionary[value];
  if (!item) return value;
  return language === "ko" ? item.ko : item.en;
}
