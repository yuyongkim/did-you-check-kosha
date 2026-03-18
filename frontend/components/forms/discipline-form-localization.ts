import { Discipline, FormFieldConfig } from "@/lib/types";

export type FormUiLanguage = "en" | "ko";

export interface DisciplineFormCopy {
  input: string;
  quickPresets: string;
  toggleOption: string;
  invalidValue: string;
  forceBlocked: string;
  resetSample: string;
  calculating: string;
  runCalculation: string;
  range: string;
  to: string;
}

const FIELD_LABEL_KO_BY_DISCIPLINE: Record<Discipline, Record<string, string>> = {
  piping: {
    material: "재질",
    temperature_profile: "온도 프로파일",
    design_pressure_mpa: "설계압력",
    design_temperature_c: "설계온도",
    nps: "공칭관경(NPS)",
    weld_type: "용접 타입",
    service_type: "서비스 타입",
    fluid_type: "유체 타입",
    corrosion_allowance_mm: "부식 여유",
    chloride_ppm: "수압시험 염화물",
    has_internal_coating: "내부 코팅",
  },
  vessel: {
    material: "재질",
    vessel_type: "용기 타입",
    design_pressure_mpa: "설계압력",
    design_temperature_c: "설계온도",
    inside_radius_mm: "내반경",
    shell_length_mm: "쉘 길이",
    straight_shell_height_mm: "직선 쉘 높이",
    head_type: "헤드 타입",
    head_depth_mm: "헤드 깊이",
    nozzle_od_mm: "노즐 외경",
    external_pressure_mpa: "외압",
    reinforcement_pad_thickness_mm: "보강패드 두께",
    reinforcement_pad_width_mm: "보강패드 폭",
    joint_efficiency: "이음 효율 (E)",
    t_current_mm: "현재 두께",
    corrosion_allowance_mm: "부식 여유",
    assumed_corrosion_rate_mm_per_year: "부식률",
  },
  rotating: {
    machine_type: "기기 타입",
    driver_type: "구동기 타입",
    service_criticality: "서비스 중요도",
    stage_count: "단수/스로우 수",
    train_arrangement: "트레인 배치",
    casing_type: "케이싱 타입",
    bearing_type: "베어링 타입",
    seal_system: "실 시스템",
    lube_system: "윤활 시스템",
    vibration_mm_per_s: "진동",
    nozzle_load_ratio: "노즐 하중비",
    bearing_temperature_c: "베어링 온도",
    lube_oil_supply_temp_c: "윤활유 공급온도",
    coupling_misalignment_mils: "커플링 미스얼라인먼트",
    speed_rpm: "회전속도",
    npsh_available_m: "NPSH 가용",
    npsh_required_m: "NPSH 요구",
    api670_coverage_pct: "API 670 커버리지",
    trip_tests_last_12m: "최근 12개월 트립시험",
    protection_bypass_active: "보호 바이패스 활성",
    axial_displacement_um: "축방향 변위",
    suction_pressure_bar: "흡입압력",
    discharge_pressure_bar: "토출압력",
    surge_events_30d: "최근 30일 서지 이벤트",
    steam_pressure_bar: "스팀 압력",
    steam_temperature_c: "스팀 온도",
    steam_quality_x: "스팀 건도(x)",
    inlet_enthalpy_kj_per_kg: "입구 엔탈피",
    outlet_enthalpy_kj_per_kg: "출구 엔탈피",
  },
  electrical: {
    equipment_type: "설비 타입",
    system_voltage_kv: "계통 전압",
    bolted_fault_current_ka: "고장전류",
    clearing_time_sec: "차단 시간",
    working_distance_mm: "작업 거리",
    breaker_interrupt_rating_ka: "차단기 정격",
    voltage_drop_percent: "전압강하",
    thd_voltage_percent: "전압 THD",
    motor_current_thd_percent: "전류 THD",
    power_factor: "역률",
    dga_score: "DGA 점수",
    oil_quality_score: "절연유 품질 점수",
    insulation_score: "절연 점수",
    load_factor_score: "부하 점수",
  },
  instrumentation: {
    instrument_type: "계장 타입",
    voting_architecture: "투표 구조",
    sil_target: "SIL 목표",
    failure_rate_per_hour: "고장률",
    proof_test_interval_hours: "증명시험 주기",
    mttr_hours: "MTTR",
    calibration_interval_days: "현재 교정 주기",
    tolerance_pct: "허용편차",
    sensor_mtbf_years: "센서 MTBF",
    cv_required: "요구 Cv",
    cv_rated: "정격 Cv",
  },
  steel: {
    member_type: "부재 타입",
    steel_grade: "강재 등급",
    section_label: "단면 라벨",
    length_m: "부재 길이",
    k_factor: "K 계수",
    radius_of_gyration_mm: "회전반경 r",
    yield_strength_mpa: "항복강도 Fy",
    gross_area_mm2: "총단면적 Ag",
    axial_demand_kn: "축력 수요",
    corrosion_loss_percent: "부식 손실",
    deflection_mm: "처짐",
    span_mm: "경간",
    connection_failure_detected: "접합부 파손 감지",
  },
  civil: {
    element_type: "요소 타입",
    environment_exposure: "노출 환경",
    fc_mpa: "압축강도 f'c",
    fy_mpa: "철근 항복강도 Fy",
    width_mm: "단면 폭 b",
    effective_depth_mm: "유효깊이 d",
    rebar_area_mm2: "철근면적 As",
    demand_moment_knm: "요구 모멘트",
    lateral_capacity_loss_percent: "횡방향 내력 손실",
    affected_area_percent: "영향 면적",
    vertical_capacity_loss_percent: "수직 내력 손실",
    carbonation_coeff_mm_sqrt_year: "탄산화 계수 k",
    service_years: "사용 연수",
    cover_thickness_mm: "피복두께",
    crack_width_mm: "균열 폭",
    spalling_area_percent: "박락 면적",
    foundation_settlement_mm: "기초 침하",
  },
};

const FIELD_HELPER_KO_BY_DISCIPLINE: Record<Discipline, Record<string, string>> = {
  piping: {
    material: "탄소강/저합금강/스테인리스/듀플렉스/니켈합금 그룹.",
    temperature_profile: "엄격 기준 또는 고온 관리 기준을 선택.",
    weld_type: "두께식에서 용접효율(E) 계수를 결정.",
    service_type: "서비스 심각도가 부식 경향에 영향.",
    fluid_type: "유체 등급별 부식 계수를 반영.",
    has_internal_coating: "내부 코팅/라이닝이 있으면 활성화.",
  },
  vessel: {
    shell_length_mm: "수평/열교환기 컨텍스트: 탄젠트 간 쉘 길이",
    straight_shell_height_mm: "수직/컬럼 컨텍스트: 직선 쉘 높이",
  },
  rotating: {
    driver_type: "압축기/펌프 트레인의 실제 구동기 아키텍처에 맞게 선택.",
    stage_count: "원심/축류는 단수, 왕복동 계열은 실린더/스트로크 수.",
    train_arrangement: "조합형 스크리닝에 사용하는 기계 트레인 배치.",
    casing_type: "무결성 및 노즐하중 보정에 반영되는 케이싱 형식.",
    bearing_type: "기본 진동 한계와 유지보수 민감도에 영향.",
    seal_system: "누출/트립 리스크 프로파일에 영향.",
    lube_system: "열 여유 및 공정 리스크 가중치에 영향.",
    npsh_available_m: "펌프/왕복동펌프 흡입 여유 체크",
    npsh_required_m: "펌프/왕복동펌프 흡입 여유 체크",
    api670_coverage_pct: "API 670 보호기능 커버리지(%)",
    protection_bypass_active: "핵심 보호 바이패스가 현재 활성 상태면 체크.",
    steam_quality_x: "침식/상변화 스크리닝을 위한 건도",
  },
  electrical: {},
  instrumentation: {},
  steel: {
    connection_failure_detected: "볼트/용접 접합부 파손이 관측되면 체크.",
  },
  civil: {},
};

const OPTION_LABEL_KO_BY_FIELD: Record<string, Record<string, string>> = {
  temperature_profile: {
    strict_process: "엄격 공정 기준(보수적)",
    high_temp_managed: "고온 관리 기준(검토 필요)",
    legacy_power_steam: "기존 발전/스팀 관리 기준",
  },
  weld_type: {
    seamless: "무계목 (E=1.0)",
    erw: "ERW (E=0.85)",
    smaw: "SMAW (E=0.85)",
    spot_rt: "부분 RT (E=0.85)",
    no_rt: "RT 없음 (E=0.80)",
  },
  service_type: {
    general: "일반",
    sour: "Sour 서비스",
    chloride: "염화물 서비스",
    high_temp: "고온 서비스",
  },
  fluid_type: {
    hydrocarbon_dry: "건식 탄화수소",
    hydrocarbon_wet: "습식 탄화수소",
    steam_condensate: "스팀 / 응축수",
    steam_superheated: "과열 스팀",
    steam_wet: "습증기",
    amine: "아민 서비스",
    h2s_sour: "H2S Sour 서비스",
    chloride_aqueous: "수용성 염화물",
    caustic: "가성소다 서비스",
    seawater: "해수",
    oxygen_rich: "산소 고농도 서비스",
  },
  vessel_type: {
    horizontal_drum: "수평 드럼",
    vertical_vessel: "수직 용기",
    column_tower: "컬럼 / 타워",
    hx_shell: "열교환기 쉘",
    reactor: "반응기",
  },
  head_type: {
    ellipsoidal_2_1: "타원형 2:1",
    torispherical: "토리구형",
    hemispherical: "반구형",
    flat: "평판형",
  },
  joint_efficiency: {
    "1.0": "타입 1 (E=1.00)",
    "0.95": "타입 1 대체 (E=0.95)",
    "0.9": "타입 2 대체 (E=0.90)",
    "0.85": "타입 2 (E=0.85)",
    "0.8": "타입 3 대체 (E=0.80)",
    "0.7": "타입 3 (E=0.70)",
    "0.6": "타입 4 (E=0.60)",
  },
  machine_type: {
    pump: "원심 펌프",
    centrifugal_compressor: "원심 압축기",
    axial_compressor: "축류 압축기",
    blower: "블로워",
    fan: "팬",
    expander: "익스팬더",
    recip_pump: "왕복동 펌프",
    screw_compressor: "스크류 압축기 (회전 PD)",
    recip_compressor: "왕복동 압축기",
    steam_turbine: "스팀 터빈",
    gas_turbine: "가스터빈",
    compressor: "압축기 (레거시 일반)",
    gearbox: "기어박스",
  },
  driver_type: {
    electric_motor_fixed: "전동기 (고정속도)",
    electric_motor_vfd: "전동기 (VFD)",
    steam_turbine_driver: "스팀터빈 구동기",
    gas_turbine_driver: "가스터빈 구동기",
    recip_engine_driver: "왕복동 엔진 구동",
    integral_prime_mover: "일체형 원동기",
  },
  service_criticality: {
    normal: "일반",
    essential: "필수",
    high_critical: "고중요",
    safety_critical: "안전중요",
  },
  train_arrangement: {
    overhung: "오버행",
    between_bearing: "베어링 사이",
    integrally_geared: "인테그럴 기어드",
    barrel: "배럴",
    inline: "인라인",
  },
  casing_type: {
    horiz_split: "수평 분할",
    vert_split: "수직 분할",
    barrel: "배럴",
    recip_frame: "왕복동 프레임",
    integral_gear_case: "일체형 기어 케이스",
  },
  bearing_type: {
    rolling_element: "구름 베어링",
    journal_tilting_pad: "저널 (틸팅패드)",
    sleeve: "슬리브",
    crosshead: "크로스헤드",
  },
  seal_system: {
    single_mech: "싱글 메카니컬",
    dual_mech: "듀얼 메카니컬",
    dry_gas_seal: "드라이 가스 실",
    packing: "패킹",
  },
  lube_system: {
    ring_oil: "링 오일",
    forced_lube: "강제 윤활",
    mist: "미스트",
    none_process_fluid: "없음 / 공정유체",
  },
  equipment_type: {
    transformer: "변압기",
    switchgear: "스위치기어",
    mcc: "MCC",
    motor: "모터",
    ups: "UPS",
    feeder_panel: "피더 패널",
    generator: "발전기",
    inverter: "인버터 / VFD",
    cable_feeder: "케이블 피더",
  },
  instrument_type: {
    pressure_transmitter: "압력 트랜스미터",
    temperature_transmitter: "온도 트랜스미터",
    flow_meter: "유량계",
    level_transmitter: "레벨 트랜스미터",
    control_valve_positioner: "제어밸브 포지셔너",
    analyzer: "분석계",
    vibration_probe: "진동 프로브",
    pressure_switch: "압력 스위치",
    thermocouple: "열전대",
    radar_level: "레이더 레벨",
    coriolis_meter: "코리올리 유량계",
  },
  voting_architecture: {
    "1oo1": "1oo1",
    "1oo2": "1oo2",
    "2oo2": "2oo2",
    "2oo3": "2oo3",
  },
  member_type: {
    column: "기둥",
    beam: "보",
    brace: "브레이스",
    girder: "거더",
    truss_member: "트러스 부재",
    pipe_rack_leg: "파이프랙 다리",
    portal_frame: "포털 프레임",
  },
  steel_grade: {
    a36: "ASTM A36",
    a572_gr50: "ASTM A572 Gr50",
    a992: "ASTM A992",
    a500_grb: "ASTM A500 GrB",
    a500_grc: "ASTM A500 GrC",
    a588: "ASTM A588",
    a913_gr65: "ASTM A913 Gr65",
    api_2w_gr50: "API 2W Gr50",
  },
  element_type: {
    beam: "보",
    column: "기둥",
    slab: "슬래브",
    foundation: "기초",
    retaining_wall: "옹벽",
    pedestal: "페데스탈",
    pile_cap: "파일캡",
    mat_foundation: "매트기초",
  },
  environment_exposure: {
    indoor_dry: "실내 건조",
    outdoor_urban: "실외 도심",
    coastal_marine: "연안 해양",
    industrial_chemical: "산업 화학",
    splash_zone: "비말 구역",
    buried_soil: "매설 토양",
    desert_hot: "사막 고온",
    freeze_thaw: "동결-융해",
    acidic_soil: "산성 토양",
    offshore: "해양 오프쇼어",
  },
};

const OPTION_GROUP_LABEL_KO_BY_TEXT: Record<string, string> = {
  "Carbon / Carbon-Mn Steel": "탄소강 / 탄소망간강",
  "Low Alloy Steel": "저합금강",
  "Stainless Steel": "스테인리스강",
  Rotodynamic: "회전형",
  "Positive Displacement": "용적형",
  "Turbomachinery / Driver": "터보기계 / 구동기",
  "Drive Train": "구동 트레인",
};

const PRESET_LABEL_KO_BY_ID: Record<string, string> = {
  "pip-general-cs": "일반 탄소강",
  "pip-legacy-steam": "기존 스팀 라인",
  "pip-sour-amine": "Sour / 아민",
  "pip-chloride-sus": "염화물 SUS",
  "ves-hdrum-standard": "수평 드럼 표준",
  "ves-column-high-temp": "고온 컬럼",
  "ves-vacuum-risk": "외압 리스크",
  "ves-nozzle-hotspot": "노즐 핫스팟",
  "rot-pump-normal": "펌프 정상",
  "rot-pump-cavitation": "펌프 캐비테이션 위험",
  "rot-compressor-vfd-alert": "원심 압축기 VFD 경보",
  "rot-compressor-steam-driver": "축류 압축기 스팀 구동",
  "rot-recip-pump-suction-risk": "왕복동 펌프 흡입 리스크",
  "rot-screw-compressor-pd": "스크류 압축기 PD",
  "rot-steam-turbine-phase": "스팀 터빈 습증기 위험",
  "rot-recip-mech": "왕복동 기계 리스크",
  "ele-transformer-normal": "변압기 정상",
  "ele-switchgear-high-arc": "스위치기어 고아크",
  "ele-vfd-harmonics": "VFD 고조파",
  "ele-breaker-mismatch": "차단기 정격 불일치",
  "ins-pressure-normal": "압력 PT 정상",
  "ins-sis-tight": "SIS 보수 기준",
  "ins-flow-drift": "유량 드리프트",
  "ins-valve-cv": "밸브 Cv 마진",
  "stl-column-normal": "기둥 정상",
  "stl-pipe-rack": "파이프랙",
  "stl-corrosion-critical": "부식 임계",
  "stl-connection-fail": "접합부 파손",
  "civ-beam-normal": "보 정상",
  "civ-marine-durability": "해양 내구성",
  "civ-substantial-damage": "중대 손상",
  "civ-settlement-alert": "침하 경보",
};

export function getDisciplineFormCopy(language: FormUiLanguage): DisciplineFormCopy {
  if (language === "ko") {
    return {
      input: "입력",
      quickPresets: "빠른 프리셋",
      toggleOption: "옵션 토글",
      invalidValue: "유효하지 않은 값",
      forceBlocked: "강제 차단 시나리오 (데모)",
      resetSample: "샘플 초기화",
      calculating: "계산 중...",
      runCalculation: "계산 실행",
      range: "범위",
      to: "~",
    };
  }

  return {
    input: "Input",
    quickPresets: "Quick Presets",
    toggleOption: "Toggle option",
    invalidValue: "Invalid value",
    forceBlocked: "Force blocked scenario (demo)",
    resetSample: "Reset Sample",
    calculating: "Calculating...",
    runCalculation: "Run Calculation",
    range: "Range",
    to: "to",
  };
}

export function localizeFieldLabel(discipline: Discipline, language: FormUiLanguage, field: FormFieldConfig): string {
  if (language !== "ko") return field.label;
  return FIELD_LABEL_KO_BY_DISCIPLINE[discipline]?.[field.name] ?? field.label;
}

export function localizeFieldHelper(
  discipline: Discipline,
  language: FormUiLanguage,
  field: FormFieldConfig,
): string | undefined {
  if (!field.helper) return undefined;
  if (language !== "ko") return field.helper;
  return FIELD_HELPER_KO_BY_DISCIPLINE[discipline]?.[field.name] ?? field.helper;
}

export function localizeOptionGroupLabel(language: FormUiLanguage, fallback: string): string {
  if (language !== "ko") return fallback;
  return OPTION_GROUP_LABEL_KO_BY_TEXT[fallback] ?? fallback;
}

export function localizeOptionLabel(
  _discipline: Discipline,
  language: FormUiLanguage,
  fieldName: string,
  optionValue: string,
  fallback: string,
): string {
  if (language !== "ko") return fallback;
  return OPTION_LABEL_KO_BY_FIELD[fieldName]?.[optionValue] ?? fallback;
}

export function localizePresetLabel(
  _discipline: Discipline,
  language: FormUiLanguage,
  presetId: string,
  fallback: string,
): string {
  if (language !== "ko") return fallback;
  return PRESET_LABEL_KO_BY_ID[presetId] ?? fallback;
}

export function localizeUnit(language: FormUiLanguage, unit: string): string {
  if (language !== "ko") return unit;
  const normalized = unit.trim();
  const map: Record<string, string> = {
    level: "등급",
    days: "일",
    years: "년",
    "mm/yr": "mm/년",
    "mm/sqrt(year)": "mm/√년",
    "kN*m": "kN·m",
    "MPa": "MPa",
    "kV": "kV",
    "kA": "kA",
    "mm/s": "mm/s",
    rpm: "rpm",
    mils: "mil",
    "/h": "/h",
    h: "h",
    mm: "mm",
    m: "m",
    C: "C",
    "%": "%",
    inch: "inch",
    mm2: "mm2",
  };
  return map[normalized] ?? unit;
}
