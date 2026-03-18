import { UiLanguage } from "@/lib/i18n";
import { CalculationResponse, Discipline, Recommendation } from "@/lib/types";

type Confidence = CalculationResponse["verification"]["confidence"];
type CalculationStatus = CalculationResponse["status"];
type VerificationLayerStatus = "pass" | "warn" | "fail";
type DisciplineHealth = "idle" | "safe" | "warning" | "critical";

const DISCIPLINE_LABEL: Record<Discipline, { en: string; ko: string }> = {
  piping: { en: "Piping", ko: "배관" },
  vessel: { en: "Static Equipment", ko: "정기기" },
  rotating: { en: "Rotating", ko: "회전기기" },
  electrical: { en: "Electrical", ko: "전기" },
  instrumentation: { en: "Instrumentation", ko: "계장" },
  steel: { en: "Steel Structure", ko: "철골구조" },
  civil: { en: "Civil Concrete", ko: "토목콘크리트" },
};

const CALC_STATUS_LABEL: Record<CalculationStatus, { en: string; ko: string }> = {
  success: { en: "SUCCESS", ko: "성공" },
  error: { en: "ERROR", ko: "오류" },
  blocked: { en: "BLOCKED", ko: "차단" },
};

const CONFIDENCE_LABEL: Record<Confidence, { en: string; ko: string }> = {
  high: { en: "HIGH", ko: "높음" },
  medium: { en: "MEDIUM", ko: "보통" },
  low: { en: "LOW", ko: "낮음" },
};

const HEALTH_LABEL: Record<DisciplineHealth, { en: string; ko: string }> = {
  idle: { en: "IDLE", ko: "대기" },
  safe: { en: "SAFE", ko: "정상" },
  warning: { en: "WARNING", ko: "주의" },
  critical: { en: "CRITICAL", ko: "위험" },
};

const VERIFICATION_LAYER_STATUS_LABEL: Record<VerificationLayerStatus, { en: string; ko: string }> = {
  pass: { en: "PASS", ko: "통과" },
  warn: { en: "WARN", ko: "주의" },
  fail: { en: "FAIL", ko: "실패" },
};

const PRIORITY_LABEL: Record<Recommendation["priority"], { en: string; ko: string }> = {
  high: { en: "HIGH", ko: "높음" },
  medium: { en: "MEDIUM", ko: "보통" },
  low: { en: "LOW", ko: "낮음" },
};

const TIMELINE_LABEL: Record<Recommendation["timeline"], { en: string; ko: string }> = {
  immediate: { en: "Immediate", ko: "즉시" },
  "1month": { en: "1 month", ko: "1개월" },
  "6months": { en: "6 months", ko: "6개월" },
  nextyear: { en: "Next year", ko: "차기 연도" },
};

const REGULATORY_CONFIDENCE_LABEL: Record<"high" | "medium" | "low", { en: string; ko: string }> = {
  high: { en: "HIGH", ko: "높음" },
  medium: { en: "MEDIUM", ko: "보통" },
  low: { en: "LOW", ko: "낮음" },
};

const VERIFICATION_LAYER_NAME_KO: Record<string, string> = {
  "Layer 1: Input Validation": "1계층: 입력 검증",
  "Layer 2: MAKER Consensus": "2계층: MAKER 합의",
  "Layer 3: Physics and Standards": "3계층: 물리/표준 검증",
  "Layer 4: Reverse Verification": "4계층: 역검증",
};

function pickLabel<T extends { en: string; ko: string }>(language: UiLanguage, value: T): string {
  return language === "ko" ? value.ko : value.en;
}

export function disciplineLabel(discipline: Discipline, language: UiLanguage): string {
  return pickLabel(language, DISCIPLINE_LABEL[discipline]);
}

export function calculationStatusLabel(status: CalculationStatus, language: UiLanguage): string {
  return pickLabel(language, CALC_STATUS_LABEL[status]);
}

export function confidenceLabel(confidence: Confidence, language: UiLanguage): string {
  return pickLabel(language, CONFIDENCE_LABEL[confidence]);
}

export function healthLabel(status: DisciplineHealth, language: UiLanguage): string {
  return pickLabel(language, HEALTH_LABEL[status]);
}

export function verificationLayerStatusLabel(status: VerificationLayerStatus, language: UiLanguage): string {
  return pickLabel(language, VERIFICATION_LAYER_STATUS_LABEL[status]);
}

export function recommendationPriorityLabel(priority: Recommendation["priority"], language: UiLanguage): string {
  return pickLabel(language, PRIORITY_LABEL[priority]);
}

export function recommendationTimelineLabel(timeline: Recommendation["timeline"], language: UiLanguage): string {
  return pickLabel(language, TIMELINE_LABEL[timeline]);
}

export function regulatoryConfidenceLabel(confidence: "high" | "medium" | "low", language: UiLanguage): string {
  return pickLabel(language, REGULATORY_CONFIDENCE_LABEL[confidence]);
}

export function verificationLayerName(layerName: string, language: UiLanguage): string {
  if (language !== "ko") return layerName;
  return VERIFICATION_LAYER_NAME_KO[layerName] ?? layerName;
}
