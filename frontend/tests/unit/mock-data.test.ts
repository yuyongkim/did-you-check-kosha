import { describe, expect, it } from "vitest";

import { buildMockCalculationResponse, isDiscipline } from "@/lib/mock-data";
import { Discipline } from "@/lib/types";

const nominalPayloads: Record<Discipline, Record<string, unknown>> = {
  piping: {
    material: "SA-106 Gr.B",
    nps: 6,
    design_pressure_mpa: 4.5,
    design_temperature_c: 250,
    thickness_history: [
      { date: "2015-01-01", thickness_mm: 10.0 },
      { date: "2020-01-01", thickness_mm: 8.6 },
      { date: "2025-01-01", thickness_mm: 7.3 },
    ],
    corrosion_allowance_mm: 1.5,
    weld_type: "seamless",
    service_type: "general",
    has_internal_coating: false,
  },
  vessel: {
    material: "SA-516-70",
    design_pressure_mpa: 2,
    design_temperature_c: 200,
    inside_radius_mm: 750,
    joint_efficiency: 0.85,
    t_current_mm: 18,
    corrosion_allowance_mm: 1.5,
    assumed_corrosion_rate_mm_per_year: 0.2,
  },
  rotating: {
    machine_type: "pump",
    vibration_mm_per_s: 2.5,
    nozzle_load_ratio: 0.85,
    bearing_temperature_c: 72,
    speed_rpm: 1800,
  },
  electrical: {
    system_voltage_kv: 13.8,
    bolted_fault_current_ka: 22,
    clearing_time_sec: 0.2,
    working_distance_mm: 455,
    breaker_interrupt_rating_ka: 31.5,
    voltage_drop_percent: 3.2,
    thd_voltage_percent: 4.8,
    dga_score: 8.2,
    oil_quality_score: 7.9,
    insulation_score: 8.3,
    load_factor_score: 7.5,
    motor_current_thd_percent: 4.5,
    power_factor: 0.91,
  },
  instrumentation: {
    sil_target: 2,
    failure_rate_per_hour: 1.0e-7,
    proof_test_interval_hours: 8760,
    mttr_hours: 8,
    calibration_interval_days: 180,
    calibration_history: [
      { days_since_ref: 0, error_pct: 0.05 },
      { days_since_ref: 90, error_pct: 0.16 },
      { days_since_ref: 180, error_pct: 0.28 },
      { days_since_ref: 270, error_pct: 0.39 },
    ],
    tolerance_pct: 1,
    sensor_mtbf_years: 8,
    cv_required: 45,
    cv_rated: 80,
    uncertainty_components_pct: [0.2, 0.3, 0.1],
  },
  steel: {
    member_type: "column",
    section_label: "W310x60",
    length_m: 6,
    k_factor: 1,
    radius_of_gyration_mm: 90,
    yield_strength_mpa: 345,
    elasticity_mpa: 200000,
    gross_area_mm2: 7600,
    corrosion_loss_percent: 8,
    axial_demand_kn: 650,
    moment_demand_knm: 90,
    deflection_mm: 10,
    span_mm: 6000,
    connection_failure_detected: false,
  },
  civil: {
    element_type: "beam",
    fc_mpa: 35,
    fy_mpa: 420,
    width_mm: 300,
    effective_depth_mm: 550,
    rebar_area_mm2: 2450,
    demand_moment_knm: 280,
    lateral_capacity_loss_percent: 8,
    affected_area_percent: 12,
    vertical_capacity_loss_percent: 6,
    carbonation_coeff_mm_sqrt_year: 1.8,
    service_years: 18,
    cover_thickness_mm: 40,
    crack_width_mm: 0.22,
    spalling_area_percent: 5,
    foundation_settlement_mm: 8,
  },
};

describe("discipline guard", () => {
  it("returns true for valid disciplines", () => {
    expect(isDiscipline("piping")).toBe(true);
    expect(isDiscipline("civil")).toBe(true);
  });

  it("returns false for invalid values", () => {
    expect(isDiscipline("invalid")).toBe(false);
    expect(isDiscipline("")).toBe(false);
  });
});

describe("mock response builder", () => {
  it("returns frontend contract for each discipline", () => {
    for (const [discipline, payload] of Object.entries(nominalPayloads)) {
      const result = buildMockCalculationResponse(discipline as Discipline, payload);
      expect(result.discipline).toBe(discipline);
      expect(result.status).toMatch(/success|blocked/);
      expect(result.details.layer_results.length).toBe(4);
      expect(Array.isArray(result.references)).toBe(true);
    }
  });

  it("forces blocked when explicit flag is set", () => {
    const result = buildMockCalculationResponse("piping", {
      ...nominalPayloads.piping,
      force_blocked: true,
    });

    expect(result.status).toBe("blocked");
    expect(result.flags.red_flags).toContain("LOG.NO_CONSENSUS_AFTER_TIEBREAKER");
  });
});
