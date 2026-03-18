# Piping NDE Recommendations by Material (Screening Guide)

## 1. Purpose
This guide explains the material-based NDE recommendation logic used in the piping workbench.

Use this as a practical screening reference.
Final inspection scope must follow site procedure, code edition, and RBI/FFS governance.

## 2. Material Group and Recommended NDE
| Material Group | Primary Methods | Targeted Methods | Main Concern |
| --- | --- | --- | --- |
| Carbon Steel | UT Thickness (CML grid) | PAUT/UT mapping, MT on selected weld details | Uniform thinning, local pitting, support/dead-leg corrosion |
| Low Alloy Steel | UT + PAUT (weld/HAZ) | MT/PT, replication metallography (hot service) | Thinning + weld-zone cracking + high-temp degradation |
| Stainless Steel | UT mapping | PT, ECT (as needed) | Chloride pitting/SCC near weld HAZ |
| Duplex Stainless | UT mapping | PT, PMI/ferrite verification | Localized corrosion + weld quality/ferrite control |
| Nickel Alloy | PT at weld root/toe | PAUT/TOFD, PMI verification | Local attack and weld-zone flaws in aggressive service |
| Unknown | UT CML baseline | PT + PMI first | Material uncertainty before mechanism-specific planning |

## 3. Cadence Recommendation Rules
- Immediate + 1-3 month follow-up:
  - temperature hard limit exceeded, or critical risk band.
- 3-6 month targeted campaign:
  - warning risk band, temperature override mode, or elevated corrosion rate.
- 6-month focused cycle:
  - moderate corrosion trend without severe flags.
- 6-12 month routine:
  - stable trend and normal risk band.

## 4. Fluid/Service Context Hints
- Chloride or seawater:
  - increase CML density at low points/dead legs;
  - for stainless/duplex, emphasize PT/ECT at weld HAZ and stagnant branches.
- Sour/H2S/amine:
  - add crack-focused weld checks and hardness verification per procedure.
- Steam service:
  - emphasize FAC-prone geometries (elbows, reducers, downstream of control valves).

## 5. Terms
- UT: Ultrasonic Testing
- PAUT: Phased Array Ultrasonic Testing
- TOFD: Time of Flight Diffraction
- PT: Liquid Penetrant Testing
- MT: Magnetic Particle Testing
- ECT: Eddy Current Testing
- PMI: Positive Material Identification
- CML: Condition Monitoring Location

## 6. Governance Note
- This guide does not supersede ASME/API code requirements.
- When uncertainty exists, escalate to SME review and FFS workflow.
