export type UiLanguage = "en" | "ko";

export type LocalizedLabel = { ko: string; en: string };

export const MACHINE_LABELS: Record<string, LocalizedLabel> = {
  steam_turbine: { ko: "스팀 터빈", en: "Steam Turbine" },
  centrifugal_compressor: { ko: "원심 압축기", en: "Centrifugal Compressor" },
  axial_compressor: { ko: "축류 압축기", en: "Axial Compressor" },
  screw_compressor: { ko: "스크류 압축기", en: "Screw Compressor" },
  recip_compressor: { ko: "왕복동 압축기", en: "Recip Compressor" },
  expander: { ko: "익스팬더", en: "Expander" },
  recip_pump: { ko: "왕복동 펌프", en: "Recip Pump" },
  pump: { ko: "펌프", en: "Pump" },
  compressor: { ko: "압축기", en: "Compressor" },
};

export const DRIVER_LABELS: Record<string, LocalizedLabel> = {
  steam_turbine_driver: { ko: "스팀터빈 구동기", en: "Steam Turbine Driver" },
  electric_motor_fixed: { ko: "전동기", en: "Electric Motor" },
  electric_motor_vfd: { ko: "VFD 전동기", en: "VFD Motor" },
  gas_engine: { ko: "가스 엔진", en: "Gas Engine" },
  diesel_engine: { ko: "디젤 엔진", en: "Diesel Engine" },
};

export const CRITICALITY_LABEL: Record<string, LocalizedLabel> = {
  normal: { ko: "일반", en: "Normal" },
  essential: { ko: "필수", en: "Essential" },
  high_critical: { ko: "고중요", en: "High Critical" },
  safety_critical: { ko: "안전중요", en: "Safety Critical" },
};

export const ARRANGEMENT_LABEL: Record<string, LocalizedLabel> = {
  overhung: { ko: "오버행", en: "Overhung" },
  between_bearing: { ko: "베어링 사이", en: "Between Bearing" },
  integrally_geared: { ko: "인테그럴 기어드", en: "Integrally Geared" },
  barrel: { ko: "배럴", en: "Barrel" },
  inline: { ko: "인라인", en: "Inline" },
};

export const CASING_LABEL: Record<string, LocalizedLabel> = {
  horiz_split: { ko: "수평 분할", en: "Horizontal Split" },
  vert_split: { ko: "수직 분할", en: "Vertical Split" },
  barrel: { ko: "배럴", en: "Barrel" },
  recip_frame: { ko: "왕복동 프레임", en: "Recip Frame" },
  integral_gear_case: { ko: "일체형 기어 케이스", en: "Integral Gear Case" },
};

export const BEARING_LABEL: Record<string, LocalizedLabel> = {
  rolling_element: { ko: "구름 베어링", en: "Rolling Element" },
  journal_tilting_pad: { ko: "저널(틸팅패드)", en: "Journal (Tilting Pad)" },
  sleeve: { ko: "슬리브", en: "Sleeve" },
  crosshead: { ko: "크로스헤드", en: "Crosshead" },
};

export const SEAL_LABEL: Record<string, LocalizedLabel> = {
  single_mech: { ko: "싱글 메카니컬", en: "Single Mechanical" },
  dual_mech: { ko: "듀얼 메카니컬", en: "Dual Mechanical" },
  dry_gas_seal: { ko: "드라이 가스 실", en: "Dry Gas Seal" },
  packing: { ko: "패킹", en: "Packing" },
};

export const LUBE_LABEL: Record<string, LocalizedLabel> = {
  ring_oil: { ko: "링 오일", en: "Ring Oil" },
  forced_lube: { ko: "강제 윤활", en: "Forced Lube" },
  mist: { ko: "미스트", en: "Mist" },
  none_process_fluid: { ko: "없음/공정유체", en: "None / Process Fluid" },
};

export interface RotatingVisualCopy {
  sectionTrain: string;
  sectionSpectrum: string;
  sectionFaultTimeline: string;
  sectionDriver: string;
  sectionProcessRisk: string;
  coupling: string;
  arrangement: string;
  stage: string;
  bearing: string;
  seal: string;
  casing: string;
  lube: string;
  machineDriverCrit: string;
  mechanical: string;
  process: string;
  protection: string;
  api670: string;
  required: string;
  bearingOilAlign: string;
  speedEnvelope: string;
  limit: string;
  protectionBypass: string;
  active: string;
  normal: string;
  vibrationLimits: string;
  nozzleLoadRatio: string;
  steamState: string;
  phaseRiskSuperheat: string;
  suctionDischarge: string;
  pressureRatioSurge: string;
  in30d: string;
  npsh: string;
  axialDisplacement: string;
  monitoringEscalation: string;
  maintenanceUrgency: string;
  adjusted: string;
  base: string;
  axisBand: string;
  axisAmplitude: string;
}

export const ROTATING_COPY: Record<UiLanguage, RotatingVisualCopy> = {
  en: {
    sectionTrain: "Machine Train Schematic",
    sectionSpectrum: "Vibration Spectrum",
    sectionFaultTimeline: "Fault Marker Timeline",
    sectionDriver: "Driver / Protection Matrix",
    sectionProcessRisk: "Process-Specific Risk",
    coupling: "Coupling",
    arrangement: "Arrangement",
    stage: "Stage",
    bearing: "Bearing",
    seal: "Seal",
    casing: "Casing",
    lube: "Lube",
    machineDriverCrit: "Machine / Driver / Criticality",
    mechanical: "Mechanical",
    process: "Process",
    protection: "Protection",
    api670: "API 670 Coverage / Trip Tests",
    required: "req",
    bearingOilAlign: "Bearing / Oil / Alignment",
    speedEnvelope: "Speed Envelope",
    limit: "limit",
    protectionBypass: "Protection Bypass",
    active: "ACTIVE",
    normal: "Normal",
    vibrationLimits: "Vibration / Limits",
    nozzleLoadRatio: "Nozzle Load Ratio",
    steamState: "Steam State (P/T/x)",
    phaseRiskSuperheat: "Phase Risk / Superheat Margin",
    suctionDischarge: "Suction / Discharge",
    pressureRatioSurge: "Pressure Ratio / Surge Events",
    in30d: "in 30d",
    npsh: "NPSH Available / Required / Margin",
    axialDisplacement: "Axial Displacement",
    monitoringEscalation: "Monitoring Cadence",
    maintenanceUrgency: "Maintenance Urgency",
    adjusted: "adj",
    base: "base",
    axisBand: "Frequency band / order",
    axisAmplitude: "Amplitude (mm/s)",
  },
  ko: {
    sectionTrain: "머신 트레인 스케매틱",
    sectionSpectrum: "진동 스펙트럼",
    sectionFaultTimeline: "결함 마커 타임라인",
    sectionDriver: "구동기 / 보호 매트릭스",
    sectionProcessRisk: "공정별 리스크",
    coupling: "커플링",
    arrangement: "배치",
    stage: "단수",
    bearing: "베어링",
    seal: "실",
    casing: "케이싱",
    lube: "윤활",
    machineDriverCrit: "기계 / 구동기 / 중요도",
    mechanical: "기계",
    process: "공정",
    protection: "보호",
    api670: "API 670 커버리지 / 트립시험",
    required: "요구",
    bearingOilAlign: "베어링 / 오일 / 정렬",
    speedEnvelope: "속도 범위",
    limit: "한계",
    protectionBypass: "보호 바이패스",
    active: "활성",
    normal: "정상",
    vibrationLimits: "진동 / 한계",
    nozzleLoadRatio: "노즐 하중비",
    steamState: "스팀 상태 (P/T/x)",
    phaseRiskSuperheat: "상변화 리스크 / 과열여유",
    suctionDischarge: "흡입 / 토출",
    pressureRatioSurge: "압력비 / 서지 이벤트",
    in30d: "최근 30일",
    npsh: "NPSH 가용 / 요구 / 여유",
    axialDisplacement: "축방향 변위",
    monitoringEscalation: "모니터링 주기",
    maintenanceUrgency: "정비 긴급도",
    adjusted: "보정",
    base: "기준",
    axisBand: "주파수 밴드 / 차수",
    axisAmplitude: "진폭 (mm/s)",
  },
};
