# User Guide (7-Discipline Design Pack)

## 1) Files
- `docs/SYSTEM_OVERVIEW.md`
- `docs/standards_index.md`
- `docs/verification_layers.md`
- `docs/golden_dataset_spec.md`
- `agents/*.md`
- `config/*`
- `golden/*.json`
- `outputs/*`
- `standards/*`
- `verification/*`

## 2) Generate Golden Specs
```powershell
python scripts/generate_three_discipline_specs.py
python scripts/generate_piping_golden_dataset.py
python scripts/generate_vessel_golden_dataset.py
python scripts/generate_rotating_golden_dataset.py
python scripts/generate_electrical_golden_dataset.py
python scripts/generate_instrumentation_golden_dataset.py
python scripts/generate_steel_golden_dataset.py
python scripts/generate_civil_golden_dataset.py
```

## 3) Validate Runtime
```powershell
python -m unittest discover -s tests -p "test_*.py"
python scripts/validate_config.py
python scripts/benchmark_all_runtime.py
python scripts/benchmark_cross_discipline.py
python scripts/benchmark_cross_discipline.py --profile all
python scripts/tune_cross_discipline_thresholds.py --rounds 50
python scripts/benchmark_five_pipeline.py
python scripts/benchmark_seven_pipeline.py
```

## 4) Integrated Execution
1. Run `python examples/mock_five_pipeline.py`.
2. Run `python examples/mock_seven_pipeline.py`.
3. Review `outputs/verification_report_runtime.md`.
4. Review `outputs/cross_discipline_report.md`.
5. Apply threshold/policy tuning for site-specific risk profile.
