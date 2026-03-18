import { describe, expect, it } from "vitest";

import { DISCIPLINE_CONFIGS } from "@/lib/mock-data";

describe("discipline config sample input types", () => {
  it("matches field types for all discipline forms", () => {
    for (const config of Object.values(DISCIPLINE_CONFIGS)) {
      for (const field of config.formFields) {
        const value = config.sampleInput[field.name];
        expect(value, `${config.discipline}.${field.name} should be defined in sampleInput`).not.toBeUndefined();

        if (field.type === "number") {
          expect(typeof value, `${config.discipline}.${field.name} should be number`).toBe("number");
        } else if (field.type === "checkbox") {
          expect(typeof value, `${config.discipline}.${field.name} should be boolean`).toBe("boolean");
        } else if (field.type === "select") {
          expect(typeof value, `${config.discipline}.${field.name} should be string`).toBe("string");
          const groupedValues = (field.optionGroups ?? []).flatMap((group) => group.options.map((item) => item.value));
          const optionValues = [...(field.options ?? []).map((item) => item.value), ...groupedValues];
          expect(
            optionValues.includes(String(value)),
            `${config.discipline}.${field.name} should match one of select options`,
          ).toBe(true);
        } else {
          expect(typeof value, `${config.discipline}.${field.name} should be string`).toBe("string");
        }
      }
    }
  });
});

describe("piping material select groups", () => {
  it("uses grouped options for CS/alloy/SUS families", () => {
    const piping = DISCIPLINE_CONFIGS.piping;
    const materialField = piping.formFields.find((field) => field.name === "material");

    expect(materialField).toBeDefined();
    expect(materialField?.type).toBe("select");
    expect(materialField?.optionGroups?.length).toBeGreaterThanOrEqual(5);

    const groupLabels = (materialField?.optionGroups ?? []).map((group) => group.label);
    expect(groupLabels).toContain("Carbon Steel (CS)");
    expect(groupLabels).toContain("Low Alloy Steel");
    expect(groupLabels).toContain("Stainless Steel (SUS)");
  });
});

describe("rotating conditional fields", () => {
  it("includes steam-only and machine-group conditional fields", () => {
    const rotating = DISCIPLINE_CONFIGS.rotating;
    const steamFields = rotating.formFields.filter((field) => field.showWhen?.field === "machine_type");

    expect(steamFields.length).toBeGreaterThanOrEqual(9);

    const steamOnly = steamFields.filter((field) => field.showWhen?.equals === "steam_turbine");
    expect(steamOnly.length).toBeGreaterThanOrEqual(5);

    const pressureRatioFields = steamFields.filter((field) => field.showWhen?.equalsAny?.includes("compressor"));
    expect(pressureRatioFields.length).toBeGreaterThanOrEqual(3);

    const pumpBranch = steamFields.filter((field) => field.showWhen?.equalsAny?.includes("pump"));
    expect(pumpBranch.length).toBeGreaterThanOrEqual(2);
    expect(pumpBranch.every((field) => field.showWhen?.equalsAny?.includes("recip_pump"))).toBe(true);
  });

  it("exposes reciprocating pump and compressor subtypes in machine options", () => {
    const rotating = DISCIPLINE_CONFIGS.rotating;
    const machineField = rotating.formFields.find((field) => field.name === "machine_type");
    const optionValues = (machineField?.optionGroups ?? []).flatMap((group) => group.options.map((option) => option.value));

    expect(optionValues).toContain("recip_pump");
    expect(optionValues).toContain("centrifugal_compressor");
    expect(optionValues).toContain("axial_compressor");
    expect(optionValues).toContain("screw_compressor");
  });

  it("exposes combination selectors for stage/train/casing/bearing/seal/lube", () => {
    const rotating = DISCIPLINE_CONFIGS.rotating;
    const stageField = rotating.formFields.find((field) => field.name === "stage_count");
    const trainField = rotating.formFields.find((field) => field.name === "train_arrangement");
    const casingField = rotating.formFields.find((field) => field.name === "casing_type");
    const bearingField = rotating.formFields.find((field) => field.name === "bearing_type");
    const sealField = rotating.formFields.find((field) => field.name === "seal_system");
    const lubeField = rotating.formFields.find((field) => field.name === "lube_system");

    expect(stageField?.type).toBe("number");
    expect(stageField?.min).toBe(1);
    expect(stageField?.max).toBeGreaterThanOrEqual(10);
    expect(trainField?.type).toBe("select");
    expect(casingField?.type).toBe("select");
    expect(bearingField?.type).toBe("select");
    expect(sealField?.type).toBe("select");
    expect(lubeField?.type).toBe("select");

    const trainOptions = (trainField?.options ?? []).map((item) => item.value);
    const casingOptions = (casingField?.options ?? []).map((item) => item.value);
    const bearingOptions = (bearingField?.options ?? []).map((item) => item.value);
    const sealOptions = (sealField?.options ?? []).map((item) => item.value);
    const lubeOptions = (lubeField?.options ?? []).map((item) => item.value);

    expect(trainOptions).toContain("integrally_geared");
    expect(casingOptions).toContain("recip_frame");
    expect(bearingOptions).toContain("crosshead");
    expect(sealOptions).toContain("dry_gas_seal");
    expect(lubeOptions).toContain("forced_lube");
  });
});
