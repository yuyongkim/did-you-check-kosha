import { CalculationResponse } from "@/lib/types";
import { toNumber } from "@/components/visualization/utils";

export type UiLanguage = "en" | "ko";
export type PipingMaterialGroup =
  | "carbon_steel"
  | "low_alloy_steel"
  | "stainless_steel"
  | "duplex_stainless"
  | "nickel_alloy"
  | "unknown";

export type RiskBand = "critical" | "warning" | "normal";

interface NdeMethod {
  method: string;
  scope: string;
  rationale: string;
}

interface NdeGuide {
  damageMode: string;
  methods: NdeMethod[];
  caution: string;
}

export const MATERIAL_GROUP_LABEL: Record<UiLanguage, Record<PipingMaterialGroup, string>> = {
  en: {
    carbon_steel: "Carbon Steel",
    low_alloy_steel: "Low Alloy Steel",
    stainless_steel: "Stainless Steel",
    duplex_stainless: "Duplex Stainless",
    nickel_alloy: "Nickel Alloy",
    unknown: "Unclassified",
  },
  ko: {
    carbon_steel: "탄소강",
    low_alloy_steel: "저합금강",
    stainless_steel: "스테인리스강",
    duplex_stainless: "듀플렉스 스테인리스",
    nickel_alloy: "니켈 합금",
    unknown: "미분류",
  },
};

const NDE_GUIDE_BY_GROUP: Record<UiLanguage, Record<Exclude<PipingMaterialGroup, "unknown">, NdeGuide>> = {
  en: {
    carbon_steel: {
      damageMode: "Uniform thinning, dead-leg pitting, and external corrosion at supports/CUI-prone spots.",
      methods: [
        {
          method: "UT Thickness (CML Grid)",
          scope: "Routine",
          rationale: "Primary thickness trend method for API 570 style remaining-life tracking.",
        },
        {
          method: "PAUT / UT Mapping",
          scope: "Targeted",
          rationale: "Use at elbows, reducers, injection points, and known turbulence zones for localized attack.",
        },
        {
          method: "MT at Weld Toe",
          scope: "As needed",
          rationale: "Surface crack screening on carbon steel attachments and high-stress weld details.",
        },
      ],
      caution: "If sour/amine risk exists, add hardness and cracking checks per site procedure and RBI plan.",
    },
    low_alloy_steel: {
      damageMode: "Thinning plus weld-zone cracking and long-term high-temperature degradation mechanisms.",
      methods: [
        {
          method: "UT / PAUT Weld-HAZ Scan",
          scope: "Routine + targeted",
          rationale: "Track thickness and detect weld-adjacent indications in elevated-temperature service.",
        },
        {
          method: "MT or PT on Welds",
          scope: "Targeted",
          rationale: "Surface crack screening at branch connections and high-restraint joints.",
        },
        {
          method: "Replication Metallography",
          scope: "High-temp program",
          rationale: "Useful for creep screening in sustained hot service where metallurgy review is required.",
        },
      ],
      caution: "For hot-service lines, align with managed high-temperature review and fitness-for-service workflow.",
    },
    stainless_steel: {
      damageMode: "Localized pitting and chloride SCC risk around weld HAZ, especially in wet chloride services.",
      methods: [
        {
          method: "UT Mapping",
          scope: "Routine",
          rationale: "Detect localized wall-loss and pitting depth distribution beyond point readings.",
        },
        {
          method: "PT (Liquid Penetrant)",
          scope: "Targeted",
          rationale: "Preferred surface crack detection approach for austenitic stainless weld zones.",
        },
        {
          method: "ECT / Surface Eddy",
          scope: "As needed",
          rationale: "Useful for thin-wall or heat-exchanger style zones where rapid crack/pit screening is needed.",
        },
      ],
      caution: "Austenitic stainless is often non-magnetic; MT sensitivity may be limited compared with PT/ECT.",
    },
    duplex_stainless: {
      damageMode: "Localized corrosion plus weld-quality/ferrite-related concerns in chloride or mixed phases.",
      methods: [
        {
          method: "UT Thickness + Mapping",
          scope: "Routine",
          rationale: "Trend wall loss and detect localized thinning at geometry changes and low points.",
        },
        {
          method: "PT on Weld Zones",
          scope: "Targeted",
          rationale: "Screen surface-connected cracking at weld toes, HAZ, and branch connections.",
        },
        {
          method: "PMI / Ferrite Check",
          scope: "Quality hold point",
          rationale: "Verifies alloy and weld condition consistency for long-term corrosion resistance.",
        },
      ],
      caution: "Maintain heat-input control and confirm duplex weld procedure compliance before accepting indications.",
    },
    nickel_alloy: {
      damageMode: "Localized attack and weld-zone cracking in aggressive chemical or high-temperature service.",
      methods: [
        {
          method: "PT on Weld Root/Toe",
          scope: "Routine targeted",
          rationale: "High-value method for surface-connected flaws in nickel-alloy weld regions.",
        },
        {
          method: "PAUT / TOFD",
          scope: "Advanced",
          rationale: "Volumetric flaw detection where conventional UT access is limited or risk is elevated.",
        },
        {
          method: "PMI Verification",
          scope: "Quality hold point",
          rationale: "Prevents alloy mix-up and supports integrity conclusions for corrosion-sensitive service.",
        },
      ],
      caution: "Use procedure-qualified probes/couplant and technician qualifications specific to nickel-alloy work.",
    },
  },
  ko: {
    carbon_steel: {
      damageMode: "균일 감육, 데드레그 피팅, 지지부/CUI 취약 구간 외면부식 위험이 큽니다.",
      methods: [
        {
          method: "UT 두께 측정 (CML 그리드)",
          scope: "정기",
          rationale: "API 570 방식 잔여수명 추적을 위한 기본 두께 트렌드 기법입니다.",
        },
        {
          method: "PAUT / UT 매핑",
          scope: "집중",
          rationale: "엘보, 리듀서, 주입부, 난류 구간 등 국부 공격 가능 부위에 적용합니다.",
        },
        {
          method: "용접 토우 MT",
          scope: "필요 시",
          rationale: "탄소강 부착부 및 고응력 용접 디테일의 표면 균열 스크리닝에 유효합니다.",
        },
      ],
      caution: "Sour/아민 리스크가 있으면 현장 절차 및 RBI 계획에 따라 경도/균열 검사를 추가하세요.",
    },
    low_alloy_steel: {
      damageMode: "감육과 함께 용접부 균열 및 장기 고온 열화 메커니즘을 함께 고려해야 합니다.",
      methods: [
        {
          method: "UT / PAUT 용접 HAZ 스캔",
          scope: "정기 + 집중",
          rationale: "고온 운전에서 두께 추이와 용접 인접부 결함 신호를 함께 추적합니다.",
        },
        {
          method: "용접부 MT 또는 PT",
          scope: "집중",
          rationale: "브랜치 접속부와 구속이 큰 이음부의 표면 균열 확인에 사용합니다.",
        },
        {
          method: "복제금속조직(Replication)",
          scope: "고온 프로그램",
          rationale: "지속 고온 운전 라인의 크리프 스크리닝에 유용합니다.",
        },
      ],
      caution: "고온 라인은 고온 관리 검토 및 FFS 워크플로와 연계해 판정하세요.",
    },
    stainless_steel: {
      damageMode: "습식 염화물 환경에서 용접 HAZ 주변 국부 피팅과 염화물 SCC 위험이 증가합니다.",
      methods: [
        {
          method: "UT 매핑",
          scope: "정기",
          rationale: "점측정만으로 놓치기 쉬운 국부 감육/피팅 분포를 확인합니다.",
        },
        {
          method: "PT (침투탐상)",
          scope: "집중",
          rationale: "오스테나이트계 스테인리스 용접부 표면 균열 검출에 우선 적용합니다.",
        },
        {
          method: "ECT / 표면 와전류",
          scope: "필요 시",
          rationale: "박육부 또는 신속 균열/피팅 스크리닝이 필요한 구간에서 유효합니다.",
        },
      ],
      caution: "오스테나이트계는 비자성인 경우가 많아 MT 민감도가 PT/ECT보다 낮을 수 있습니다.",
    },
    duplex_stainless: {
      damageMode: "염화물 또는 혼상 환경에서 국부 부식과 용접 품질/페라이트 관련 이슈를 점검해야 합니다.",
      methods: [
        {
          method: "UT 두께 + 매핑",
          scope: "정기",
          rationale: "형상 변화부 및 저점부 국부 감육을 포함해 두께 트렌드를 관리합니다.",
        },
        {
          method: "용접부 PT",
          scope: "집중",
          rationale: "용접 토우, HAZ, 브랜치 접속부의 표면 연결 균열을 확인합니다.",
        },
        {
          method: "PMI / 페라이트 점검",
          scope: "품질 홀드포인트",
          rationale: "합금 및 용접 상태 일관성을 확인해 장기 내식성 판단을 보강합니다.",
        },
      ],
      caution: "지시 수용 전 듀플렉스 용접 절차 준수 및 열입력 관리 상태를 확인하세요.",
    },
    nickel_alloy: {
      damageMode: "공격성 화학환경/고온 운전에서 국부 공격 및 용접부 균열 가능성이 존재합니다.",
      methods: [
        {
          method: "용접 루트/토우 PT",
          scope: "정기 집중",
          rationale: "니켈 합금 용접부의 표면 연결 결함 확인에 효과가 큽니다.",
        },
        {
          method: "PAUT / TOFD",
          scope: "고급",
          rationale: "일반 UT 접근성이 낮거나 리스크가 높은 구간의 체적 결함 검출에 사용합니다.",
        },
        {
          method: "PMI 검증",
          scope: "품질 홀드포인트",
          rationale: "합금 혼입을 방지하고 부식 민감 서비스의 무결성 결론을 뒷받침합니다.",
        },
      ],
      caution: "니켈 합금 전용 절차, 탐촉자/커플런트, 자격 요건을 갖춘 검사 체계를 사용하세요.",
    },
  },
};

const UNKNOWN_GROUP_NDE_GUIDE: Record<UiLanguage, NdeGuide> = {
  en: {
    damageMode: "Material group unknown. Use conservative mixed-method screening until material is confirmed.",
    methods: [
      {
        method: "UT Thickness (CML Grid)",
        scope: "Routine",
        rationale: "Establish baseline wall-loss trend independent of exact alloy.",
      },
      {
        method: "PT on Welds",
        scope: "Targeted",
        rationale: "Surface crack screening when material magnetism and mechanism are uncertain.",
      },
      {
        method: "PMI Verification",
        scope: "Priority",
        rationale: "Confirm actual material family before finalizing inspection strategy.",
      },
    ],
    caution: "Confirm MTR/PMI first. Material identification should precede final NDE scope approval.",
  },
  ko: {
    damageMode: "재질군이 불명확합니다. 재질 확인 전까지 보수적 혼합 기법으로 스크리닝하세요.",
    methods: [
      {
        method: "UT 두께 측정 (CML 그리드)",
        scope: "정기",
        rationale: "정확한 합금 정보와 무관하게 초기 벽두께 손실 추세를 확보합니다.",
      },
      {
        method: "용접부 PT",
        scope: "집중",
        rationale: "자성/손상 메커니즘이 불확실할 때 표면 균열을 우선 스크리닝합니다.",
      },
      {
        method: "PMI 검증",
        scope: "우선",
        rationale: "최종 검사전략 확정 전 실제 재질군을 먼저 확인합니다.",
      },
    ],
    caution: "MTR/PMI를 먼저 확인한 뒤 최종 NDE 범위를 승인하세요.",
  },
};

export const PIPING_COPY: Record<UiLanguage, {
  sectionCross: string;
  sectionTrend: string;
  sectionNde: string;
  labelOd: string;
  labelIdCurrent: string;
  labelIdAtMin: string;
  labelRl: string;
  labelCurrentThickness: string;
  labelCr: string;
  labelTminLimit: string;
  labelHoopStress: string;
  labelHoopRatio: string;
  labelHydrotest: string;
  xAxisHint: string;
  fluidContext: string;
  tempEnvelope: string;
  gridAverage: string;
  forecast: string;
  limitYear: (year: number) => string;
  materialGroup: string;
  suggestedNdeCadence: string;
  ndeTerms: string;
  unknown: string;
  now: string;
  yearUnit: string;
  rateUnit: string;
  axisInspection: string;
  axisThickness: string;
}> = {
  en: {
    sectionCross: "Pipe Cross-Section (Dynamic)",
    sectionTrend: "Corrosion Progress Trend and Limit Forecast",
    sectionNde: "API 570 Grid, Life and NDE Recommendation",
    labelOd: "OD",
    labelIdCurrent: "ID(current)",
    labelIdAtMin: "ID@t_min",
    labelRl: "RL",
    labelCurrentThickness: "t_current",
    labelCr: "CR",
    labelTminLimit: "t_min limit",
    labelHoopStress: "Hoop Stress (screen)",
    labelHoopRatio: "Hoop Utilization",
    labelHydrotest: "Hydrotest Pressure",
    xAxisHint: "X-axis shows inspection sequence labels. If date exists, it is shown as `YY-MM`; otherwise `T1/T2/T3` means ordered thickness records.",
    fluidContext: "Fluid Context",
    tempEnvelope: "Temp Envelope",
    gridAverage: "Grid Average / Utilization",
    forecast: "Forecast",
    limitYear: (year) => `Limit year around ${year}`,
    materialGroup: "Material / Group",
    suggestedNdeCadence: "Suggested NDE Cadence",
    ndeTerms: "NDE terms: UT=Ultrasonic, PAUT=Phased Array UT, TOFD=Time of Flight Diffraction, PT=Penetrant, MT=Magnetic Particle, ECT=Eddy Current.",
    unknown: "unknown",
    now: "Now",
    yearUnit: "y",
    rateUnit: "mm/y",
    axisInspection: "Inspection point / date",
    axisThickness: "Wall thickness (mm)",
  },
  ko: {
    sectionCross: "배관 단면 (동적)",
    sectionTrend: "부식 진행 추세 및 한계 예측",
    sectionNde: "API 570 그리드, 잔여수명 및 NDE 권고",
    labelOd: "외경(OD)",
    labelIdCurrent: "내경(현재)",
    labelIdAtMin: "내경(t_min 기준)",
    labelRl: "잔여수명(RL)",
    labelCurrentThickness: "현재두께",
    labelCr: "부식률(CR)",
    labelTminLimit: "t_min 한계",
    labelHoopStress: "후프응력 (스크리닝)",
    labelHoopRatio: "후프 사용률",
    labelHydrotest: "수압시험 압력",
    xAxisHint: "X축은 검사 이력 순서입니다. 날짜가 있으면 `YY-MM`, 없으면 `T1/T2/T3` 순번으로 표시됩니다.",
    fluidContext: "유체 컨텍스트",
    tempEnvelope: "온도 관리 범위",
    gridAverage: "그리드 평균 / 사용률",
    forecast: "예측",
    limitYear: (year) => `한계 도달 예상 연도: ${year}년`,
    materialGroup: "재질 / 재질군",
    suggestedNdeCadence: "권장 NDE 주기",
    ndeTerms: "NDE 약어: UT=초음파, PAUT=위상배열초음파, TOFD=회절시간법, PT=침투탐상, MT=자분탐상, ECT=와전류.",
    unknown: "미확인",
    now: "현재",
    yearUnit: "년",
    rateUnit: "mm/년",
    axisInspection: "검사 지점 / 날짜",
    axisThickness: "벽두께 (mm)",
  },
};

function formatInspectionLabel(rawDate: unknown, index: number): string {
  if (typeof rawDate !== "string" || rawDate.trim().length === 0) return `T${index + 1}`;

  const parsed = new Date(rawDate);
  if (Number.isNaN(parsed.getTime())) return `T${index + 1}`;

  const yy = String(parsed.getFullYear()).slice(2);
  const mm = String(parsed.getMonth() + 1).padStart(2, "0");
  return `${yy}-${mm}`;
}

export function historyData(result: CalculationResponse | null, language: UiLanguage): Array<{ name: string; thickness: number }> {
  const rows = Array.isArray(result?.details.input_data.thickness_history) ? result?.details.input_data.thickness_history : [];
  if (!rows.length) {
    return language === "ko"
      ? [
        { name: "10년전", thickness: 10 },
        { name: "5년전", thickness: 8.6 },
        { name: "현재", thickness: 7.3 },
      ]
      : [
        { name: "Y-10", thickness: 10 },
        { name: "Y-5", thickness: 8.6 },
        { name: "Now", thickness: 7.3 },
      ];
  }

  return rows.map((row, index) => ({
    name: formatInspectionLabel((row as { date?: string }).date, index),
    thickness: toNumber((row as { thickness_mm?: number }).thickness_mm, 0),
  }));
}

export function normalizeMaterialGroup(materialOrGroupRaw: string): PipingMaterialGroup {
  const normalized = materialOrGroupRaw.toUpperCase();

  if (normalized.includes("CARBON_STEEL")) return "carbon_steel";
  if (normalized.includes("LOW_ALLOY_STEEL")) return "low_alloy_steel";
  if (normalized.includes("STAINLESS_STEEL")) return "stainless_steel";
  if (normalized.includes("DUPLEX_STAINLESS")) return "duplex_stainless";
  if (normalized.includes("NICKEL_ALLOY")) return "nickel_alloy";

  if (normalized.includes("S31803") || normalized.includes("S32205") || normalized.includes("S32750")) return "duplex_stainless";
  if (normalized.includes("TP304") || normalized.includes("TP304L") || normalized.includes("TP316") || normalized.includes("TP316L")) {
    return "stainless_steel";
  }
  if (normalized.includes("TP321") || normalized.includes("TP347")) return "stainless_steel";
  if (normalized.includes("P11") || normalized.includes("P22") || normalized.includes("P5") || normalized.includes("P9") || normalized.includes("P91")) {
    return "low_alloy_steel";
  }
  if (normalized.includes("N08825") || normalized.includes("N06625") || normalized.includes("N04400") || normalized.includes("ALLOY")) {
    return "nickel_alloy";
  }
  if (normalized.includes("SA-106") || normalized.includes("A106") || normalized.includes("SA-53") || normalized.includes("API 5L")) {
    return "carbon_steel";
  }
  return "unknown";
}

export function recommendedNdeCadence(
  language: UiLanguage,
  riskBand: RiskBand,
  corrosionRate: number,
  temperatureMode: string,
): string {
  if (language === "ko") {
    if (temperatureMode === "exceeded_hard_limit" || riskBand === "critical") return "즉시 검사 + 1~3개월 추적";
    if (temperatureMode === "override_review_required" || riskBand === "warning" || corrosionRate >= 0.5) return "3~6개월 집중 캠페인";
    if (corrosionRate >= 0.2) return "6개월 주기(핫스팟 집중)";
    return "6~12개월 정기 주기";
  }

  if (temperatureMode === "exceeded_hard_limit" || riskBand === "critical") return "Immediate + 1-3 month follow-up";
  if (temperatureMode === "override_review_required" || riskBand === "warning" || corrosionRate >= 0.5) return "3-6 month targeted campaign";
  if (corrosionRate >= 0.2) return "6-month cycle with focused hotspots";
  return "6-12 month routine cycle";
}

export function processHint(
  language: UiLanguage,
  fluidTypeRaw: string,
  materialGroup: PipingMaterialGroup,
  temperatureMode: string,
): string {
  const fluid = fluidTypeRaw.toLowerCase();
  if (language === "ko") {
    if (temperatureMode === "exceeded_hard_limit") {
      return "온도가 관리 한계를 초과했습니다. 고급 NDE와 FFS 검토로 즉시 승격하세요.";
    }
    if (fluid.includes("chloride") || fluid.includes("seawater")) {
      if (materialGroup === "stainless_steel" || materialGroup === "duplex_stainless") {
        return "염화물 환경: 용접 HAZ, 저점부, 정체 브랜치의 PT/ECT를 우선 배치하세요(SCC 위험).";
      }
      return "염화물 환경: 저점부, 데드레그, 혼합 구간의 UT CML 밀도를 높이세요.";
    }
    if (fluid.includes("h2s") || fluid.includes("sour") || fluid.includes("amine")) {
      return "Sour/아민 서비스: 절차에 따라 용접 균열 스크리닝과 경도 확인을 포함하세요.";
    }
    if (fluid.includes("steam")) {
      return "스팀 서비스: 엘보, 리듀서, 제어밸브 하류 FAC 취약부를 집중 점검하세요.";
    }
    return "기본 점검: 부식 핫스팟, 데드레그, 지지부, 형상 변화부.";
  }

  if (temperatureMode === "exceeded_hard_limit") {
    return "Temperature is beyond managed limit. Escalate to advanced NDE plus fitness-for-service review.";
  }
  if (fluid.includes("chloride") || fluid.includes("seawater")) {
    if (materialGroup === "stainless_steel" || materialGroup === "duplex_stainless") {
      return "Chloride environment: prioritize PT/ECT at weld HAZ, low points, and stagnant branches (SCC risk).";
    }
    return "Chloride environment: increase UT CML density at low points, dead legs, and mixing zones.";
  }
  if (fluid.includes("h2s") || fluid.includes("sour") || fluid.includes("amine")) {
    return "Sour/amine service: include weld crack screening and hardness verification per procedure.";
  }
  if (fluid.includes("steam")) {
    return "Steam service: focus FAC-prone elbows, reducers, and downstream of control valves.";
  }
  return "Baseline focus: corrosion hotspots, dead legs, supports, and geometry transitions.";
}

export function mapTemperatureProfileLabel(language: UiLanguage, profile: string): string {
  if (language !== "ko") return profile.replace(/_/g, " ");
  if (profile === "strict_process") return "엄격 공정";
  if (profile === "high_temp_managed") return "고온 관리";
  if (profile === "legacy_power_steam") return "기존 발전/스팀";
  return profile.replace(/_/g, " ");
}

export function mapFluidTypeLabel(language: UiLanguage, fluidType: string, unknownLabel: string): string {
  if (fluidType === "unknown") return unknownLabel;
  return fluidType.replace(/_/g, " ");
}

export function getNdeGuide(language: UiLanguage, materialGroup: PipingMaterialGroup): NdeGuide {
  return materialGroup === "unknown" ? UNKNOWN_GROUP_NDE_GUIDE[language] : NDE_GUIDE_BY_GROUP[language][materialGroup];
}
