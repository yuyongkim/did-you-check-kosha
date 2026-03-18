import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface CalculationGuideItem {
  tag: string;
  name: string;
  route: string;
  what: string;
  keyInputs: string[];
  keyOutputs: string[];
  standards: string[];
  decision: string;
}

const CALCULATION_GUIDE: CalculationGuideItem[] = [
  {
    tag: "PIP",
    name: "Piping",
    route: "/piping",
    what: "배관 최소요구두께, 부식률, 잔여수명(RL), 검사주기를 계산합니다.",
    keyInputs: ["재질/유체", "설계압력/온도", "두께 이력(T1,T2,T3)"],
    keyOutputs: ["t_min_mm", "cr_selected_mm_per_year", "remaining_life_years", "inspection_interval_years"],
    standards: ["ASME B31.3", "API 570"],
    decision: "운전 지속/교체시점/검사주기 단축 여부",
  },
  {
    tag: "VES",
    name: "Static Equipment (Vessel)",
    route: "/vessel",
    what: "쉘/헤드 필요두께, 외압 활용도, 노즐보강 적정성을 스크리닝합니다.",
    keyInputs: ["직경/두께", "압력/온도", "재질강도/허용응력"],
    keyOutputs: ["t_required_shell_mm", "external_pressure_utilization", "nozzle_reinforcement_index", "remaining_life_years"],
    standards: ["ASME Section VIII", "API 510"],
    decision: "계속 사용/보강 필요/재평가 필요",
  },
  {
    tag: "ROT",
    name: "Rotating",
    route: "/rotating",
    what: "펌프/압축기 계열에서 진동허용치와 기계/공정/보호상태를 계산합니다.",
    keyInputs: ["기기타입(원심/왕복 등)", "구동타입", "진동/운전/트립 정보"],
    keyOutputs: ["adjusted_vibration_limit_mm_per_s", "mechanical_integrity_index", "process_stability_index", "protection_readiness_index"],
    standards: ["API 610/617/618/674", "API 670"],
    decision: "정상 모니터링/강화 모니터링/즉시 개입",
  },
  {
    tag: "ELE",
    name: "Electrical",
    route: "/electrical",
    what: "아크플래시, 고장전류, 차단기 정격 여유, 전압강하를 스크리닝합니다.",
    keyInputs: ["계통전압/단락전류", "차단기 정격", "케이블 길이/부하"],
    keyOutputs: ["arc_flash_energy_cal_cm2", "fault_current_ka", "breaker_interrupt_rating_ka", "voltage_drop_percent"],
    standards: ["NFPA 70E (개념)", "IEC/현장 사내 기준"],
    decision: "보호협조/설정 변경/위험저감 조치",
  },
  {
    tag: "INS",
    name: "Instrumentation",
    route: "/instrumentation",
    what: "SIS 루프의 PFDavg, 달성 SIL, 드리프트 추세, 교정주기를 평가합니다.",
    keyInputs: ["루프 구조/시험주기", "고장률 추정", "계측 드리프트 데이터"],
    keyOutputs: ["pfdavg", "sil_achieved", "predicted_drift_pct", "calibration_interval_optimal_days"],
    standards: ["IEC 61511", "ISA/SIS 실무"],
    decision: "현행 유지/교정주기 단축/루프 개선",
  },
  {
    tag: "STL",
    name: "Steel Structure",
    route: "/steel",
    what: "부재의 D/C 비율과 안정성 지표를 계산해 구조 안전여유를 봅니다.",
    keyInputs: ["부재 형상/길이", "축력/휨", "재질강도"],
    keyOutputs: ["dc_ratio", "lambda_c", "phi_pn_kn", "deflection_mm"],
    standards: ["AISC", "현장 구조기준"],
    decision: "유지/보강/긴급 구조검토",
  },
  {
    tag: "CIV",
    name: "Civil Concrete",
    route: "/civil",
    what: "콘크리트 부재의 내구열화(탄산화/균열)와 손상등급을 계산합니다.",
    keyInputs: ["피복두께", "균열폭/환경", "재령/노출조건"],
    keyOutputs: ["dc_ratio", "carbonation_depth_mm", "years_to_corrosion_init", "substantial_damage"],
    standards: ["ACI", "국내 유지관리 기준"],
    decision: "모니터링/보수계획/즉시 보수",
  },
];

export default function CalculationGuidePage() {
  return (
    <main className="flex-1 p-3">
      <section className="rounded-lg border border-border bg-card p-5">
        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">What This System Calculates</p>
        <h1 className="mt-2 text-2xl font-semibold text-secondary">공종별 계산 범위와 결과 해석 가이드</h1>
        <p className="mt-2 max-w-5xl text-sm text-muted-foreground">
          아래 표는 이 시스템이 각 공종에서 어떤 입력을 받아 무엇을 계산하고, 어떤 유지보수 의사결정에 연결되는지 요약한 페이지입니다.
        </p>
      </section>

      <section className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {CALCULATION_GUIDE.map((item) => (
          <Card key={item.tag} className="group h-full transition-colors hover:border-primary/60">
            <CardHeader>
              <CardTitle>
                [{item.tag}] {item.name}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-sm text-foreground/90">{item.what}</p>

              <div>
                <p className="text-xs uppercase tracking-wide text-primary">Key Inputs</p>
                <ul className="mt-1 space-y-1 text-sm text-foreground/90">
                  {item.keyInputs.map((input) => (
                    <li key={input}>- {input}</li>
                  ))}
                </ul>
              </div>

              <div>
                <p className="text-xs uppercase tracking-wide text-primary">Key Outputs</p>
                <ul className="mt-1 space-y-1 text-sm text-foreground/90">
                  {item.keyOutputs.map((output) => (
                    <li key={output} className="font-mono text-[12px]">{output}</li>
                  ))}
                </ul>
              </div>

              <div>
                <p className="text-xs uppercase tracking-wide text-primary">Reference Standards</p>
                <p className="mt-1 text-sm text-foreground/90">{item.standards.join(" | ")}</p>
              </div>

              <div className="rounded-[6px] border border-border bg-muted px-2 py-1">
                <p className="text-xs text-muted-foreground">Decision Point</p>
                <p className="text-sm text-foreground/90">{item.decision}</p>
              </div>

              <Link
                href={item.route}
                className="inline-flex w-full items-center justify-between rounded-[6px] border border-primary/40 bg-primary/10 px-3 py-2 text-sm font-semibold text-primary transition-colors hover:bg-primary hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
              >
                <span>Open {item.name} Workbench</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
              <p className="text-[11px] text-muted-foreground">Clickable: opens the workbench page.</p>
            </CardContent>
          </Card>
        ))}
      </section>
    </main>
  );
}
