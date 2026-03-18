import type { GlossaryDiscipline } from "@/lib/glossary-types";
import { STANDARD_GLOSSARY } from "@/lib/standards-content";
import type { StandardDeepGuidance, StandardGlossaryEntry } from "@/lib/standards-types";
import { formatStandardReference, standardPriority } from "@/lib/standards-utils";

export type { StandardDeepGuidance, StandardGlossaryEntry } from "@/lib/standards-types";
export { formatStandardReference };

export function getStandardGlossaryEntries(discipline: GlossaryDiscipline = "all"): StandardGlossaryEntry[] {
  const scoped = discipline === "all"
    ? [...STANDARD_GLOSSARY]
    : STANDARD_GLOSSARY.filter((entry) => entry.disciplines.includes(discipline) || entry.disciplines.includes("common"));
  scoped.sort((a, b) => {
    const priorityDiff = standardPriority(a, discipline) - standardPriority(b, discipline);
    if (priorityDiff !== 0) return priorityDiff;
    return a.code.localeCompare(b.code);
  });
  return scoped;
}

export function getStandardDeepGuidance(code: string): StandardDeepGuidance {
  const normalized = String(code ?? "").toUpperCase();

  if (normalized.includes("UG-27")) {
    return {
      engineeringIntent: "Prevent pressure-containing shell failure by enforcing a conservative minimum thickness basis.",
      practicalUse: "Use early in design/re-rating to confirm that selected shell thickness still has margin after corrosion allowance and efficiency factors.",
      whatToVerify: [
        "Design pressure/temperature basis is latest approved",
        "Correct radius/diameter basis and weld efficiency category",
        "Corrosion allowance and mill tolerance treatment is consistent",
      ],
      commonMisses: [
        "Using nominal instead of effective thickness in margin checks",
        "Mixing units when converting MPa/bar and mm/inch",
      ],
    };
  }

  if (normalized.includes("UG-28")) {
    return {
      engineeringIntent: "Avoid external-pressure instability/buckling where membrane-stress checks alone are insufficient.",
      practicalUse: "Apply when vacuum, jacket, or external pressure exists; screen utilization before detailed FEA or code chart iterations.",
      whatToVerify: [
        "Effective unsupported length/span assumptions",
        "Stiffening ring spacing and boundary condition realism",
        "Corrosion-thinned thickness at worst location",
      ],
      commonMisses: [
        "Ignoring local thinning hot spots in buckling-critical zones",
        "Using internal-pressure criteria for external-pressure cases",
      ],
    };
  }

  if (normalized.includes("UG-37")) {
    return {
      engineeringIntent: "Ensure local area removed by opening/nozzle is adequately replaced by reinforcement.",
      practicalUse: "Use for nozzle additions, rerates, and debottleneck reviews where opening loads and corrosion may have reduced effective area.",
      whatToVerify: [
        "Opening geometry and reinforcement zone limits",
        "Available vs required area accounting method",
        "Pad/shell/nozzle thickness actually available after corrosion",
      ],
      commonMisses: [
        "Double-counting reinforcement contribution",
        "Using fabrication nominal thickness instead of measured minimum",
      ],
    };
  }

  if (normalized.includes("PARA 304.1.2")) {
    return {
      engineeringIntent: "Set minimum process-piping wall thickness for pressure design with code factors.",
      practicalUse: "Primary check for line classes and MOC changes; combine with corrosion-rate trend for life and interval planning.",
      whatToVerify: [
        "Allowable stress source and temperature basis",
        "Weld efficiency and Y-factor selection",
        "Outside diameter/NPS mapping and dimensional basis",
      ],
      commonMisses: [
        "Incorrect E-factor for weld category/RT scope",
        "Forgetting added allowances when comparing against current thickness",
      ],
    };
  }

  if (normalized.includes("TABLE A-1")) {
    return {
      engineeringIntent: "Provide temperature-dependent allowable stress values needed by pressure design equations.",
      practicalUse: "Treat as governing material-property table in piping/vessel checks; verify grade and temperature bins before every rerun.",
      whatToVerify: [
        "Exact material grade/spec alignment with project class",
        "Interpolation/extrapolation policy at boundary temperatures",
        "Edition consistency across all connected calculations",
      ],
      commonMisses: [
        "Using near-grade substitute allowable without documented basis",
        "Applying out-of-range values without management of change review",
      ],
    };
  }

  if (normalized.includes("API 570")) {
    return {
      engineeringIntent: "Control in-service piping risk through inspection strategy, corrosion evaluation, and interval governance.",
      practicalUse: "Use to convert measured thickness history into corrosion rate, remaining life, and next-inspection windows.",
      whatToVerify: [
        "Thickness history quality and date spacing",
        "Damage mechanism relevance (CUI, sulfidation, chloride, etc.)",
        "Interval cap and risk ranking alignment with site policy",
      ],
      commonMisses: [
        "Over-trusting short-term CR spikes without data quality checks",
        "Setting interval by habit instead of remaining-life evidence",
      ],
    };
  }

  if (normalized.includes("API 510")) {
    return {
      engineeringIntent: "Maintain pressure-vessel fitness-for-service between turnarounds via structured inspection and repair control.",
      practicalUse: "Use for in-service vessel interval, damage review, and repair/re-rate decision workflow.",
      whatToVerify: [
        "Damage mechanism mapping to inspection method",
        "Minimum required thickness vs current measured minimum",
        "RBI/inspection interval rationale and approvals",
      ],
      commonMisses: [
        "Treating localized thinning as uniform corrosion in life calculations",
        "Missing repair traceability and post-repair baseline reset",
      ],
    };
  }

  if (normalized.includes("API 610")) {
    return {
      engineeringIntent: "Assure centrifugal pump mechanical reliability through standardized design and acceptance expectations.",
      practicalUse: "Use for pump train baseline limits, nozzle-load screening, and vibration condition interpretation.",
      whatToVerify: [
        "Machine category and duty match selected limits",
        "Nozzle load ratio and alignment status",
        "Vibration trend against corrected baseline",
      ],
      commonMisses: [
        "Comparing unlike operating points without speed/load normalization",
        "Ignoring NPSH margin contribution in vibration diagnosis",
      ],
    };
  }

  if (normalized.includes("API 674")) {
    return {
      engineeringIntent: "Control reciprocating pump integrity risk under pulsation-heavy cyclic loading conditions.",
      practicalUse: "Use for reciprocating pump trains where suction margin, pulsation, and valve dynamics can drive reliability loss.",
      whatToVerify: [
        "Suction condition margin and pulsation damping configuration",
        "Crosshead/bearing lubrication and temperature trends",
        "Protection coverage and trip-test evidence for critical services",
      ],
      commonMisses: [
        "Applying centrifugal pump acceptance logic directly to reciprocating pumps",
        "Ignoring low-flow/high-pulsation operation in risk screening",
      ],
    };
  }

  if (normalized.includes("API 617")) {
    return {
      engineeringIntent: "Ensure axial/centrifugal compressor trains meet robust mechanical integrity requirements.",
      practicalUse: "Use when evaluating compressor train risk from vibration, pressure ratio, and axial behavior.",
      whatToVerify: [
        "Compressor type/section and operating envelope",
        "Pressure ratio and surge-event history",
        "Axial displacement and bearing condition trends",
      ],
      commonMisses: [
        "Treating anti-surge events as nuisance alarms instead of degradation signals",
        "Ignoring driver-machine interaction effects on limits",
      ],
    };
  }

  if (normalized.includes("API 618")) {
    return {
      engineeringIntent: "Control reciprocating compressor mechanical risk under cyclic loads and pulsation-sensitive operation.",
      practicalUse: "Use for recip-specific vibration/load/axial screening and maintenance prioritization.",
      whatToVerify: [
        "Rod load and cyclic severity context",
        "Pulsation/surge-like instability indicators",
        "Temperature and lubrication condition at bearings/crossheads",
      ],
      commonMisses: [
        "Applying centrifugal compressor heuristics directly to recip machines",
        "Underestimating alignment/coupling effects on reliability",
      ],
    };
  }

  if (normalized.includes("API 619")) {
    return {
      engineeringIntent: "Standardize rotary positive-displacement compressor package integrity and reliability behavior.",
      practicalUse: "Use for screw/lobe-type machine risk review where load and thermal behavior differ from dynamic compressors.",
      whatToVerify: [
        "Driver matching and package integration limits",
        "Thermal condition and lubrication stability",
        "Vibration pattern consistency with machine topology",
      ],
      commonMisses: [
        "Using generic vibration thresholds without machine-context correction",
        "Missing thermal-lubrication interactions during upset conditions",
      ],
    };
  }

  if (normalized.includes("API 672")) {
    return {
      engineeringIntent: "Define integration quality for packaged/integrally geared compressor assemblies.",
      practicalUse: "Use for packaged unit acceptance and lifecycle checks where vendor package boundaries matter.",
      whatToVerify: [
        "Package interface completeness (controls/protection/lube)",
        "Driver-gear-compressor alignment and commissioning data",
        "Protection coverage and periodic test discipline",
      ],
      commonMisses: [
        "Assuming package vendor defaults meet site criticality requirements",
        "Losing traceability of package-level protection overrides",
      ],
    };
  }

  if (normalized.includes("API 611") || normalized.includes("API 612")) {
    return {
      engineeringIntent: "Ensure steam turbine drivers are configured for stable, maintainable train operation.",
      practicalUse: "Use when compressor/pump trains are steam-driven and steam-state quality affects erosion and trip risk.",
      whatToVerify: [
        "Steam quality and superheat margin",
        "Energy-drop consistency and operating mode",
        "Protection readiness and bypass status",
      ],
      commonMisses: [
        "Ignoring wetness risk during transient/low-load operation",
        "Treating steam condition alarms as non-mechanical events",
      ],
    };
  }

  if (normalized.includes("API 616")) {
    return {
      engineeringIntent: "Define gas turbine driver requirements and integration expectations for rotating trains.",
      practicalUse: "Use for high-speed driver trains where thermal behavior and protection response are critical.",
      whatToVerify: [
        "Speed envelope adherence and transient excursions",
        "Driver-train coupling and alignment status",
        "Trip logic coverage and test frequency",
      ],
      commonMisses: [
        "Underestimating startup/shutdown transient contribution to damage",
        "Incomplete mapping of turbine-side alarms to train risk",
      ],
    };
  }

  if (normalized.includes("API 670")) {
    return {
      engineeringIntent: "Protect rotating machinery through reliable monitoring, alarm, and trip architecture.",
      practicalUse: "Use as minimum protection governance: channel coverage, bypass control, and proof/trip testing.",
      whatToVerify: [
        "Coverage percentage for required protection functions",
        "Trip-test frequency vs criticality target",
        "Bypass status and compensating controls",
      ],
      commonMisses: [
        "Leaving bypass active without formal risk acceptance",
        "Coverage metric reported high but key channels unavailable",
      ],
    };
  }

  if (normalized.includes("ISO 20816-3")) {
    return {
      engineeringIntent: "Classify machine vibration severity zones for condition interpretation and response.",
      practicalUse: "Use as severity-language bridge between raw vibration numbers and action thresholds.",
      whatToVerify: [
        "Machine class and mounting context",
        "Measurement location and signal quality",
        "Trend movement across severity zones",
      ],
      commonMisses: [
        "Comparing readings from inconsistent measurement points",
        "Using single snapshot instead of trend-based judgment",
      ],
    };
  }

  if (normalized.includes("IEEE 1584")) {
    return {
      engineeringIntent: "Estimate incident energy and arc-flash boundary for electrical safety decisions.",
      practicalUse: "Use for PPE selection, labeling, and mitigation prioritization based on realistic fault/clearing parameters.",
      whatToVerify: [
        "Fault current and clearing time basis validity",
        "Working distance and electrode configuration assumptions",
        "Study model update after protection setting changes",
      ],
      commonMisses: [
        "Using stale protection clearing times after relay updates",
        "Applying one generic working distance across all equipment",
      ],
    };
  }

  if (normalized.includes("IEC 61511")) {
    return {
      engineeringIntent: "Manage SIS lifecycle so target risk reduction is achieved and sustained.",
      practicalUse: "Use for SIL target/achieved traceability, proof-test strategy, and functional safety governance.",
      whatToVerify: [
        "PFDavg model assumptions and architecture factor",
        "Proof-test interval and test coverage realism",
        "Bypass/override management in operations",
      ],
      commonMisses: [
        "Assuming SIL target met without current proof-test evidence",
        "Ignoring maintenance-induced unavailability in lifecycle reviews",
      ],
    };
  }

  if (normalized.includes("AISC 360")) {
    return {
      engineeringIntent: "Ensure steel members and systems satisfy strength, stability, and serviceability requirements.",
      practicalUse: "Use for D/C, slenderness, and deflection checks in ongoing integrity screening.",
      whatToVerify: [
        "Effective length and boundary condition assumptions",
        "Section loss/corrosion impact on area and inertia",
        "Demand combination and load path consistency",
      ],
      commonMisses: [
        "Evaluating capacity with original section after corrosion loss",
        "Using inconsistent load combinations across members",
      ],
    };
  }

  if (normalized.includes("ACI 318") || normalized.includes("ACI 562")) {
    return {
      engineeringIntent: "Maintain concrete member safety via capacity checks and deterioration-aware assessment.",
      practicalUse: "Use for flexural D/C and durability triggers such as carbonation, cracking, and spalling.",
      whatToVerify: [
        "Material strengths and reinforcement details",
        "Demand-capacity ratio for governing section",
        "Durability indicators (cover, carbonation depth, crack/spall state)",
      ],
      commonMisses: [
        "Treating durability findings as cosmetic while capacity is degrading",
        "Ignoring environment-specific deterioration acceleration",
      ],
    };
  }

  return {
    engineeringIntent: "Provide a conservative, auditable engineering baseline for integrity decisions.",
    practicalUse: "Use together with project basis, measured data, and site governance to make release decisions.",
    whatToVerify: [
      "Scope/applicability of the selected code edition",
      "Input data quality and unit consistency",
      "Decision traceability to inspection/test evidence",
    ],
    commonMisses: [
      "Applying a clause outside its intended scope",
      "Using derived numbers without recording assumptions",
    ],
  };
}
