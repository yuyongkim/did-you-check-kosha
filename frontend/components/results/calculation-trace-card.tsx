import { BlockMath, InlineMath } from "react-katex";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { getTermDefinition, getTermLabel } from "@/lib/glossary";
import { formatStandardReference } from "@/lib/standards";
import { CalculationResponse } from "@/lib/types";

const RESERVED_WORDS = new Set([
  "if",
  "pass",
  "lookup",
  "table",
  "max",
  "min",
  "sum",
  "code",
  "penalty",
  "within",
  "and",
  "or",
  "with",
]);

const GREEK_WORDS = new Set(["lambda", "phi", "pi", "theta", "alpha", "beta", "gamma", "delta"]);
const FUNCTION_WORDS = new Set(["min", "max", "sum", "lookup", "table", "penalty", "code"]);

const TOKEN_LATEX_MAP: Record<string, string> = {
  "D/C": "\\frac{D}{C}",
  "f'c": "f'_c",
  phiPn: "\\phi P_n",
  phiMn: "\\phi M_n",
  PFDavg: "\\mathrm{PFD}_{avg}",
  RL: "\\mathrm{RL}",
  HI: "\\mathrm{HI}",
};

const SYMBOL_MEANINGS: Record<string, string> = {
  P: "Design pressure.",
  D: "Pipe diameter or governing diameter.",
  R: "Inside radius.",
  S: "Allowable stress.",
  E: "Weld joint efficiency.",
  Y: "Code coefficient for the thickness equation.",
  CA: "Corrosion allowance.",
  CR: "Corrosion rate.",
  CR_long: "Long-term corrosion rate.",
  CR_short: "Short-term corrosion rate.",
  CR_selected: "Conservative selected corrosion rate.",
  t_req: "Required thickness without corrosion allowance.",
  t_min: "Minimum required thickness with corrosion allowance.",
  t_required: "Required thickness from governing vessel equation.",
  t_current: "Current measured thickness.",
  RL: "Remaining life.",
  TI: "Proof test interval.",
  MTTR: "Mean time to repair.",
  PFDavg: "Average probability of failure on demand.",
  architecture_factor: "Adjustment factor for voting architecture.",
  P_u: "Factored axial demand.",
  M_u: "Factored moment demand.",
  phiPn: "Design axial strength, phi*Pn.",
  phiMn: "Design moment strength, phi*Mn.",
  lambda: "Failure rate or lambda variable.",
  lambda_c: "Non-dimensional slenderness.",
  Fcr: "Critical buckling stress.",
  Fy: "Yield strength.",
  As: "Area of steel reinforcement.",
  b: "Section width.",
  d: "Effective depth or working distance depending on equation context.",
  a: "Equivalent compression block depth.",
  E_arc: "Arc-flash incident energy.",
  I_fault: "Fault current.",
  t_clear: "Clearing time.",
  Xc: "Carbonation depth.",
  k: "Carbonation coefficient.",
  cover: "Concrete cover depth.",
  adjusted_vibration_limit_mm_per_s: "Vibration alert limit adjusted by machine, driver, and criticality factors.",
  driver_factor: "Driver-dependent adjustment factor for dynamic limit screening.",
  criticality_factor: "Criticality-based tightening factor for conservative limits.",
  mechanical_integrity_index: "0-10 mechanical integrity score from vibration/load/temperature/displacement penalties.",
  process_stability_index: "0-10 process stability score from surge, pressure ratio, NPSH, and phase-state risk.",
  protection_readiness_index: "0-10 readiness score from API 670 coverage, trip tests, and bypass state.",
  api670_coverage_pct: "Percent of expected API 670 monitoring/protection functions currently available.",
  trip_tests_last_12m: "Executed protection trip tests over the last 12 months.",
  protection_bypass_active: "Whether any key protection bypass is currently active.",
  pressure_ratio: "Compressor discharge-to-suction pressure ratio.",
  surge_events_30d: "Number of surge or surge-proximity events in the last 30 days.",
  npsh_margin_m: "NPSH available minus required margin used for cavitation screening.",
};

const SYMBOL_MEANINGS_KO: Record<string, string> = {
  P: "설계압력.",
  D: "배관 직경 또는 지배 직경.",
  R: "내반경.",
  S: "허용응력.",
  E: "용접 효율 계수.",
  Y: "두께식 코드 계수.",
  CA: "부식 여유.",
  CR: "부식률.",
  CR_long: "장기 부식률.",
  CR_short: "단기 부식률.",
  CR_selected: "보수적으로 선택된 부식률.",
  t_req: "부식 여유 제외 요구두께.",
  t_min: "부식 여유 포함 최소요구두께.",
  t_required: "지배 식에서 계산된 요구두께.",
  t_current: "현재 측정두께.",
  RL: "잔여수명.",
  TI: "증명시험 주기.",
  MTTR: "평균 복구시간.",
  PFDavg: "수요 시 평균 고장확률.",
  architecture_factor: "투표구조 보정계수.",
  P_u: "계수축력 수요.",
  M_u: "계수모멘트 수요.",
  phiPn: "설계 축강도, phi*Pn.",
  phiMn: "설계 휨강도, phi*Mn.",
  lambda: "고장률 또는 람다 변수.",
  lambda_c: "무차원 세장비.",
  Fcr: "임계 좌굴응력.",
  Fy: "항복강도.",
  As: "철근 단면적.",
  b: "단면 폭.",
  d: "식 맥락에 따른 유효깊이 또는 작업거리.",
  a: "등가 압축블록 깊이.",
  E_arc: "아크플래시 입사에너지.",
  I_fault: "고장전류.",
  t_clear: "차단 시간.",
  Xc: "탄산화 깊이.",
  k: "탄산화 계수.",
  cover: "피복두께.",
  adjusted_vibration_limit_mm_per_s: "기계/구동기/중요도를 반영한 보정 진동 경보한계.",
  driver_factor: "구동기 유형 보정계수.",
  criticality_factor: "중요도 기반 보수화 계수.",
  mechanical_integrity_index: "진동/하중/온도/변위 패널티를 합산한 0-10 기계 무결성 지수.",
  process_stability_index: "서지/압력비/NPSH/상태 리스크를 반영한 0-10 공정 안정성 지수.",
  protection_readiness_index: "API 670 커버리지, 트립시험, 바이패스 상태를 반영한 0-10 준비도 지수.",
  api670_coverage_pct: "필요 API 670 계측/보호 기능 대비 현재 가용 비율.",
  trip_tests_last_12m: "최근 12개월 보호 트립시험 실행 횟수.",
  protection_bypass_active: "핵심 보호 기능 바이패스 활성 여부.",
  pressure_ratio: "컴프레서 토출/흡입 압력비.",
  surge_events_30d: "최근 30일 서지(또는 근접) 이벤트 횟수.",
  npsh_margin_m: "캐비테이션 스크리닝용 NPSH 여유.",
};

function normalizeFormula(formula: string): string {
  return formula
    .replace(/\s*<=\s*/g, " <= ")
    .replace(/\s*>=\s*/g, " >= ")
    .replace(/\s*!=\s*/g, " != ")
    .replace(/\s*=\s*/g, " = ")
    .replace(/\s*\+\s*/g, " + ")
    .replace(/\s*-\s*/g, " - ")
    .replace(/\s*\*\s*/g, " * ")
    .replace(/\s*\/\s*/g, " / ")
    .replace(/\s+/g, " ")
    .trim();
}

function splitFormulaLines(formula: string): string[] {
  if (!formula || formula.startsWith("[see backend")) return [formula];
  return normalizeFormula(formula)
    .split(";")
    .map((line) => line.trim())
    .filter(Boolean);
}

function stripOuterParentheses(expression: string): string {
  const text = expression.trim();
  if (!text.startsWith("(") || !text.endsWith(")")) return text;

  let depth = 0;
  for (let idx = 0; idx < text.length; idx += 1) {
    const ch = text[idx];
    if (ch === "(") depth += 1;
    if (ch === ")") depth -= 1;
    if (depth === 0 && idx < text.length - 1) return text;
  }
  return text.slice(1, -1).trim();
}

function countTopLevelOperators(expression: string): Record<string, number> {
  const counts: Record<string, number> = { "+": 0, "-": 0, "*": 0, "/": 0 };
  let depth = 0;
  for (let idx = 0; idx < expression.length; idx += 1) {
    const ch = expression[idx];
    if (ch === "(") depth += 1;
    if (ch === ")") depth = Math.max(0, depth - 1);
    if (depth === 0 && Object.prototype.hasOwnProperty.call(counts, ch)) counts[ch] += 1;
  }
  return counts;
}

function findTopLevelDivisionIndex(expression: string): number {
  let depth = 0;
  for (let idx = 0; idx < expression.length; idx += 1) {
    const ch = expression[idx];
    if (ch === "(") depth += 1;
    if (ch === ")") depth = Math.max(0, depth - 1);
    if (depth === 0 && ch === "/") return idx;
  }
  return -1;
}

function parseSimpleFraction(expression: string): { numerator: string; denominator: string } | null {
  const candidate = stripOuterParentheses(expression);
  const operatorCounts = countTopLevelOperators(candidate);
  const isPureFraction = operatorCounts["/"] === 1
    && operatorCounts["+"] === 0
    && operatorCounts["-"] === 0;

  if (!isPureFraction) return null;

  const divisionIndex = findTopLevelDivisionIndex(candidate);
  if (divisionIndex < 0) return null;

  const numerator = candidate.slice(0, divisionIndex).trim();
  const denominator = candidate.slice(divisionIndex + 1).trim();
  if (!numerator || !denominator) return null;

  return { numerator, denominator };
}

function tokenToLatex(token: string): string {
  if (TOKEN_LATEX_MAP[token]) return TOKEN_LATEX_MAP[token];

  const subscriptMatch = token.match(/^([A-Za-z][A-Za-z0-9]*)_([A-Za-z0-9]+)$/);
  if (subscriptMatch) {
    const base = tokenToLatex(subscriptMatch[1]);
    return `${base}_{${subscriptMatch[2]}}`;
  }

  const normalized = token.toLowerCase();
  if (GREEK_WORDS.has(normalized)) return `\\${normalized}`;
  if (FUNCTION_WORDS.has(normalized)) return `\\operatorname{${normalized}}`;
  if (/^[A-Za-z]$/.test(token)) return token;
  if (/^[A-Za-z][A-Za-z0-9]*$/.test(token)) return `\\mathrm{${token}}`;
  return token;
}

function toLatexInline(expression: string): string {
  let result = "";
  let idx = 0;

  while (idx < expression.length) {
    const twoChars = expression.slice(idx, idx + 2);
    if (twoChars === "<=") {
      result += " \\le ";
      idx += 2;
      continue;
    }
    if (twoChars === ">=") {
      result += " \\ge ";
      idx += 2;
      continue;
    }
    if (twoChars === "!=") {
      result += " \\neq ";
      idx += 2;
      continue;
    }

    const ch = expression[idx];

    if (ch === "*") {
      result += " \\cdot ";
      idx += 1;
      continue;
    }
    if (ch === ",") {
      result += ", ";
      idx += 1;
      continue;
    }

    const tokenMatch = expression.slice(idx).match(/^[A-Za-z][A-Za-z0-9_']*/);
    if (tokenMatch) {
      result += tokenToLatex(tokenMatch[0]);
      idx += tokenMatch[0].length;
      continue;
    }

    result += ch;
    idx += 1;
  }

  return result.replace(/\s+/g, " ").trim();
}

function escapeLatexText(text: string): string {
  return text
    .replace(/\\/g, "\\textbackslash{}")
    .replace(/([{}$%&#_^~])/g, "\\$1");
}

function toLatexExpression(expression: string): string {
  const trimmed = stripOuterParentheses(expression);
  const fraction = parseSimpleFraction(trimmed);
  if (fraction) {
    return `\\frac{${toLatexExpression(fraction.numerator)}}{${toLatexExpression(fraction.denominator)}}`;
  }
  return toLatexInline(trimmed);
}

function toLatexLine(line: string): string {
  if (!line || line.startsWith("[")) return `\\text{${escapeLatexText(line || "N/A")}}`;

  const lower = line.toLowerCase();
  if (lower.includes("pass if")) {
    return `\\text{${escapeLatexText(line)}}`;
  }

  const equalIndex = line.indexOf(" = ");
  if (equalIndex < 0) return toLatexExpression(line);

  const lhs = line.slice(0, equalIndex);
  const rhs = line.slice(equalIndex + 3);
  return `${toLatexExpression(lhs)} = ${toLatexExpression(rhs)}`;
}

function extractSymbols(formulaLines: string[]): string[] {
  const seen = new Set<string>();
  const symbols: string[] = [];

  for (const line of formulaLines) {
    const tokens = line.match(/[A-Za-z][A-Za-z0-9_']*/g) ?? [];
    for (const token of tokens) {
      const normalized = token.toLowerCase();
      if (RESERVED_WORDS.has(normalized)) continue;
      if (!seen.has(token)) {
        seen.add(token);
        symbols.push(token);
      }
    }
  }

  return symbols.slice(0, 14);
}

function getSymbolMeaning(symbol: string, language: "en" | "ko"): { label: string; description: string } {
  const localizedMap = language === "ko" ? SYMBOL_MEANINGS_KO : SYMBOL_MEANINGS;
  return {
    label: getTermLabel(symbol, symbol),
    description: localizedMap[symbol] ?? getTermDefinition(symbol),
  };
}

function formulaHint(formula: string, language: "en" | "ko"): string | null {
  if (formula.includes("t_req") || formula.includes("t_min")) {
    return language === "ko"
      ? "두께식은 압력, 직경/반경, 허용응력, 용접효율, 부식여유를 함께 반영합니다."
      : "Thickness equations combine pressure, diameter/radius, allowable stress, weld efficiency, and corrosion allowance.";
  }
  if (formula.includes("RL")) {
    return language === "ko"
      ? "잔여수명은 두께 여유를 선택 부식률로 나눈 값입니다."
      : "Remaining life is thickness margin divided by selected corrosion rate.";
  }
  if (formula.includes("PFDavg")) {
    return language === "ko"
      ? "PFDavg는 SIS 무결성 검증에 사용하는 수요 시 평균 고장확률입니다."
      : "PFDavg is average probability of failure on demand for SIS integrity checks.";
  }
  if (formula.includes("D/C")) {
    return language === "ko"
      ? "D/C가 1을 초과하면 수요가 설계용량을 초과한 상태입니다."
      : "D/C greater than 1 indicates demand exceeds design capacity.";
  }
  if (formula.includes("mechanical_integrity_index")) {
    return language === "ko"
      ? "기계 무결성 지수는 진동, 하중, 온도, 변위, 정렬 패널티를 통합한 지표입니다."
      : "Mechanical integrity index aggregates vibration, load, temperature, displacement, and alignment penalties.";
  }
  if (formula.includes("protection_readiness_index")) {
    return language === "ko"
      ? "보호 준비도 지수는 API 670 커버리지, 트립시험 이행, 바이패스 상태를 반영합니다."
      : "Protection readiness index reflects API 670 coverage, trip-test discipline, and bypass status.";
  }
  if (formula.includes("process_stability_index")) {
    return language === "ko"
      ? "공정 안정성 지수는 서지 경향, 압력비, NPSH 여유, 스팀 상태 리스크를 스크리닝합니다."
      : "Process stability index screens surge tendency, pressure ratio, NPSH margin, and steam-state risk.";
  }
  return null;
}

export function CalculationTraceCard({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const copy = language === "ko"
    ? {
        title: "계산 추적",
        empty: "계산 실행 후 추적 정보가 표시됩니다.",
        step: "단계",
        formula: "수식",
        symbolMeanings: "기호 설명",
        reference: "근거 표준",
      }
    : {
        title: "Calculation Trace",
        empty: "Trace appears after calculation run.",
        step: "Step",
        formula: "Formula",
        symbolMeanings: "Symbol Meanings",
        reference: "Reference",
      };

  return (
    <Card className="animate-fadeUp">
      <CardHeader>
        <CardTitle>{copy.title}</CardTitle>
      </CardHeader>
      <CardContent>
        {!result && <p className="text-sm text-muted-foreground">{copy.empty}</p>}
        {result && (
          <div className="space-y-3">
            {result.details.calculation_steps.map((step) => {
              const lines = splitFormulaLines(step.formula_used);
              const symbols = extractSymbols(lines);

              return (
                <div key={step.step_number} className="rounded-[6px] border border-border bg-card p-3">
                  <p className="text-xs uppercase tracking-wide text-muted-foreground">{copy.step} {step.step_number}</p>
                  <p className="mt-1 text-sm font-medium text-foreground">{step.description}</p>
                  <p className="mt-1 text-xs text-muted-foreground">{copy.formula}</p>
                  <div className="rounded-[6px] border border-border bg-muted px-2 py-1 text-foreground">
                    {lines.map((line, idx) => (
                      <div key={`${step.step_number}-formula-${idx}`} className="overflow-x-auto py-0.5">
                        <BlockMath math={toLatexLine(line)} errorColor="#ef4444" />
                      </div>
                    ))}
                  </div>

                  {symbols.length > 0 && (
                    <div className="mt-2 rounded-[6px] border border-border bg-card px-2 py-2">
                      <p className="text-[11px] uppercase tracking-wide text-muted-foreground">{copy.symbolMeanings}</p>
                      <div className="mt-1 grid gap-1 md:grid-cols-2">
                        {symbols.map((symbol) => {
                          const meaning = getSymbolMeaning(symbol, language);
                          return (
                            <div key={`${step.step_number}-${symbol}`} className="grid grid-cols-[120px_1fr] items-start gap-2">
                              <span className="font-data text-xs font-semibold text-foreground">
                                <InlineMath math={toLatexExpression(symbol)} />
                              </span>
                              <span className="text-[11px] text-muted-foreground">
                                {meaning.label}: {meaning.description}
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {formulaHint(step.formula_used, language) && (
                    <p className="mt-1 text-[11px] text-muted-foreground">{formulaHint(step.formula_used, language)}</p>
                  )}
                  <p className="text-xs text-muted-foreground">{copy.reference}: {formatStandardReference(step.standard_reference)}</p>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
