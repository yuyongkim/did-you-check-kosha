import { describe, expect, it } from "vitest";

import { buildMockCalculationResponse } from "@/lib/mock-data";

describe("rotating mock expansion", () => {
  it("flags reciprocating pump cavitation when NPSH margin is negative", () => {
    const result = buildMockCalculationResponse("rotating", {
      machine_type: "recip_pump",
      driver_type: "recip_engine_driver",
      service_criticality: "essential",
      vibration_mm_per_s: 6.1,
      nozzle_load_ratio: 1.08,
      bearing_temperature_c: 89,
      lube_oil_supply_temp_c: 74,
      coupling_misalignment_mils: 2.8,
      speed_rpm: 420,
      npsh_available_m: 2.2,
      npsh_required_m: 3.4,
      api670_coverage_pct: 88,
      trip_tests_last_12m: 2,
      protection_bypass_active: false,
    });

    expect(result.flags.red_flags).toContain("PHY.PUMP_CAVITATION_RISK");
    expect(result.status).toBe("blocked");
    expect(result.results.npsh_margin_m).toBeLessThan(0);
  });

  it("flags compressor protection bypass and surge criticality", () => {
    const result = buildMockCalculationResponse("rotating", {
      machine_type: "axial_compressor",
      driver_type: "steam_turbine_driver",
      service_criticality: "safety_critical",
      vibration_mm_per_s: 6.2,
      nozzle_load_ratio: 1.16,
      bearing_temperature_c: 96,
      lube_oil_supply_temp_c: 86,
      coupling_misalignment_mils: 5.8,
      axial_displacement_um: 124,
      speed_rpm: 12800,
      suction_pressure_bar: 2.1,
      discharge_pressure_bar: 19.8,
      surge_events_30d: 6,
      api670_coverage_pct: 72,
      trip_tests_last_12m: 1,
      protection_bypass_active: true,
    });

    expect(result.flags.red_flags).toContain("STD.API670_BYPASS_ACTIVE");
    expect(result.flags.red_flags).toContain("PHY.ROTATING_SURGE_CRITICAL");
    expect(result.status).toBe("blocked");
    expect(Number(result.results.protection_readiness_index)).toBeLessThan(5);
  });

  it("flags rotary PD compressor ratio and event risk", () => {
    const result = buildMockCalculationResponse("rotating", {
      machine_type: "screw_compressor",
      driver_type: "electric_motor_fixed",
      service_criticality: "essential",
      vibration_mm_per_s: 5.8,
      nozzle_load_ratio: 1.08,
      bearing_temperature_c: 93,
      lube_oil_supply_temp_c: 87,
      coupling_misalignment_mils: 5.2,
      axial_displacement_um: 72,
      speed_rpm: 5200,
      suction_pressure_bar: 1.6,
      discharge_pressure_bar: 13.2,
      surge_events_30d: 6,
      api670_coverage_pct: 80,
      trip_tests_last_12m: 2,
      protection_bypass_active: false,
    });

    expect(result.flags.red_flags).toContain("PHY.ROTATING_SURGE_CRITICAL");
    expect(result.status).toBe("blocked");
    expect(Number(result.results.pressure_ratio)).toBeGreaterThan(8);
  });

  it("returns success for healthy rotating baseline", () => {
    const result = buildMockCalculationResponse("rotating", {
      machine_type: "pump",
      driver_type: "electric_motor_fixed",
      service_criticality: "normal",
      vibration_mm_per_s: 2.4,
      nozzle_load_ratio: 0.84,
      bearing_temperature_c: 71,
      lube_oil_supply_temp_c: 56,
      coupling_misalignment_mils: 1.8,
      speed_rpm: 1780,
      npsh_available_m: 5.8,
      npsh_required_m: 3.9,
      api670_coverage_pct: 96,
      trip_tests_last_12m: 4,
      protection_bypass_active: false,
    });

    expect(result.status).toBe("success");
    expect(result.flags.red_flags.length).toBe(0);
    expect(Number(result.results.mechanical_integrity_index)).toBeGreaterThanOrEqual(7);
    expect(Number(result.results.protection_readiness_index)).toBeGreaterThanOrEqual(7);
  });

  it("warns on incompatible stage/casing/lube combination", () => {
    const result = buildMockCalculationResponse("rotating", {
      machine_type: "axial_compressor",
      driver_type: "electric_motor_fixed",
      service_criticality: "normal",
      stage_count: 2,
      train_arrangement: "integrally_geared",
      casing_type: "recip_frame",
      bearing_type: "journal_tilting_pad",
      seal_system: "dry_gas_seal",
      lube_system: "none_process_fluid",
      vibration_mm_per_s: 2.1,
      nozzle_load_ratio: 0.8,
      bearing_temperature_c: 70,
      lube_oil_supply_temp_c: 54,
      speed_rpm: 6000,
      suction_pressure_bar: 2.8,
      discharge_pressure_bar: 8.2,
      surge_events_30d: 0,
      api670_coverage_pct: 96,
      trip_tests_last_12m: 4,
      protection_bypass_active: false,
    });

    expect(result.status).toBe("success");
    expect(result.flags.warnings).toContain("LOG.STAGE_COUNT_MACHINE_MISMATCH");
    expect(result.flags.warnings).toContain("LOG.CASING_MACHINE_MISMATCH");
    expect(result.flags.warnings).toContain("LOG.LUBE_MACHINE_MISMATCH");
  });
});
