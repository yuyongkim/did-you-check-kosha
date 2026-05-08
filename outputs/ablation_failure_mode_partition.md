# Cross-Discipline Ablation: Failure-Mode Partition

- Profile: tuned_round_50
- Total Scenarios: 60
- Total Blocked: 26

## Per-Family Counts (primary family per blocked scenario)

| Family | Count | Share |
|---|---:|---:|
| Piping/Vessel nozzle-margin family | 22 | 0.8462 |
| Electrical/Rotating bearing-coupling family | 3 | 0.1154 |
| Civil/Rotating foundation-vibration family | 1 | 0.0385 |
| Other (unclassified) | 0 | 0.0000 |
| **Sum** | **26** | |

## Blocked Scenarios (per-row family assignment)

| Set | Scenario | Primary Family | Per-Family Blocking Counts | Blocking Codes |
|---|---:|---|---|---|
| aligned_boundary | 1 | Piping/Vessel nozzle-margin family | electrical_rotating_bearing=1, piping_vessel_nozzle=4 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK |
| aligned_boundary | 2 | Piping/Vessel nozzle-margin family | electrical_rotating_bearing=1, piping_vessel_nozzle=3 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK |
| aligned_boundary | 3 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=4 | PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK |
| aligned_boundary | 4 | Piping/Vessel nozzle-margin family | electrical_rotating_bearing=1, piping_vessel_nozzle=2 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD |
| aligned_boundary | 5 | Piping/Vessel nozzle-margin family | electrical_rotating_bearing=1, piping_vessel_nozzle=6 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK |
| aligned_boundary | 6 | Piping/Vessel nozzle-margin family | electrical_rotating_bearing=1, piping_vessel_nozzle=3 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK |
| aligned_failure | 1 | Civil/Rotating foundation-vibration family | civil_rotating_foundation=3, electrical_rotating_bearing=2, piping_vessel_nozzle=2 | PHY.ELECTRICAL_NOISE_TO_SIS_RISK, PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.FOUNDATION_CRACK_VIBRATION_COUPLING, PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK |
| aligned_failure | 2 | Piping/Vessel nozzle-margin family | civil_rotating_foundation=3, electrical_rotating_bearing=2, piping_vessel_nozzle=8 | PHY.ELECTRICAL_NOISE_TO_SIS_RISK, PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.FOUNDATION_CRACK_VIBRATION_COUPLING, PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK, PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK, PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK, PHY.VIBRATION_TO_PIPING_STRESS_RISK |
| aligned_failure | 3 | Piping/Vessel nozzle-margin family | civil_rotating_foundation=2, electrical_rotating_bearing=1, piping_vessel_nozzle=8 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.FOUNDATION_CRACK_VIBRATION_COUPLING, PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK, PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK, PHY.VIBRATION_TO_PIPING_STRESS_RISK |
| aligned_failure | 4 | Piping/Vessel nozzle-margin family | civil_rotating_foundation=2, electrical_rotating_bearing=1, piping_vessel_nozzle=2 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.FOUNDATION_CRACK_VIBRATION_COUPLING, PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD |
| mixed_first20 | 16 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=1 | PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK |
| mixed_first20 | 19 | Piping/Vessel nozzle-margin family | electrical_rotating_bearing=1, piping_vessel_nozzle=2 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK |
| mixed_first20 | 20 | Piping/Vessel nozzle-margin family | electrical_rotating_bearing=1, piping_vessel_nozzle=2 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD |
| mixed_random20 | 1 | Piping/Vessel nozzle-margin family | civil_rotating_foundation=1, electrical_rotating_bearing=1, piping_vessel_nozzle=2 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK |
| mixed_random20 | 2 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=2 | PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD |
| mixed_random20 | 5 | Electrical/Rotating bearing-coupling family | civil_rotating_foundation=1, electrical_rotating_bearing=2, piping_vessel_nozzle=1 | PHY.ELECTRICAL_NOISE_TO_SIS_RISK, PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK |
| mixed_random20 | 6 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=2 | PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK, PHY.NOZZLE_INTERFACE_OVERLOAD |
| mixed_random20 | 8 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=2 | PHY.NOZZLE_INTERFACE_OVERLOAD |
| mixed_random20 | 10 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=1 | PHY.NOZZLE_INTERFACE_OVERLOAD |
| mixed_random20 | 12 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=2 | PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK |
| mixed_random20 | 14 | Electrical/Rotating bearing-coupling family | electrical_rotating_bearing=1 | PHY.ELECTRICAL_NOISE_TO_SIS_RISK |
| mixed_random20 | 15 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=4 | PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK, PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK |
| mixed_random20 | 17 | Electrical/Rotating bearing-coupling family | electrical_rotating_bearing=1 | PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK |
| mixed_random20 | 18 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=2 | PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK |
| mixed_random20 | 19 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=3 | PHY.NOZZLE_INTERFACE_OVERLOAD, PHY.VIBRATION_TO_PIPING_STRESS_RISK |
| mixed_random20 | 20 | Piping/Vessel nozzle-margin family | piping_vessel_nozzle=1 | PHY.NOZZLE_INTERFACE_OVERLOAD |
