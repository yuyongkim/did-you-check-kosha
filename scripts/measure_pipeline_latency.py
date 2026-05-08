#!/usr/bin/env python3
"""End-to-end pipeline latency measurement.

Goal (manuscript §6.7 / R1 deployment-feasibility follow-up): for the
"compliance co-pilot during design review" claim to be credible, the
pipeline must be fast enough to use interactively. This script measures
median and p95 latency in milliseconds across:

  1. Layered verification stack (Layer 1..4 combined, per discipline)
  2. Per-layer breakdown for piping (Layer 1 input validation,
     Layer 2 K-voting, Layer 3 physics/standards, Layer 4 reverse checks)
  3. Cross-discipline validator (one paired call across all 7 disciplines)
  4. KOSHA RAG retrieval (top-10)
  5. KOSHA RAG generation (Qwen via Ollama; skipped if unreachable)

Per-stage measurement is repeated 5 times; we report the median and
p95 of the 5 samples.

Notes
-----
- Per-layer breakdown is only emitted for piping because each discipline
  service exposes its layer methods under different private names; the
  full `service.evaluate()` call for the other 6 disciplines is the
  comparable "Layers 1-4 combined" measurement.
- If Ollama (http://127.0.0.1:11434) is not reachable, the generation
  step is reported as "skipped" and the rest of the report still emits.
"""

from __future__ import annotations

import json
import platform
import statistics
import sys
import urllib.error
import urllib.request
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Dict, List, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.benchmark_all_runtime import DATASETS
from src.civil.service import CivilVerificationService
from src.cross_discipline import CrossDisciplineThresholds, CrossDisciplineValidator
from src.electrical.service import ElectricalVerificationService
from src.instrumentation.service import InstrumentationVerificationService
from src.piping.models import parse_piping_input
from src.piping.service import PipingVerificationService
from src.rag.local_kosha_rag import (
    DEFAULT_INDEX_PATH,
    build_prompt,
    connect_db,
    generate_with_ollama,
    search_index,
)
from src.rotating.service import RotatingVerificationService
from src.steel.service import SteelVerificationService
from src.vessel.service import VesselVerificationService
from scripts.benchmark_cross_discipline import build_payload


OUT_JSON = ROOT / "outputs" / "pipeline_latency.json"
OUT_MD = ROOT / "outputs" / "pipeline_latency.md"

REPS = 5
OLLAMA_HOST = "http://127.0.0.1:11434"
OLLAMA_GEN_URL = f"{OLLAMA_HOST}/api/generate"
# Qwen model preference order; whichever is locally installed first wins.
# Falls back to "skip generation" if none are present.
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b-instruct",
    "qwen3:4b",
    "qwen3:8b",
    "qwen2.5:3b",
)
RAG_QUERY = "pressure vessel remaining life assessment"
RAG_TOPK = 10


def first_standard_case(dataset_path: Path) -> Mapping[str, Any]:
    data = json.loads(dataset_path.read_text(encoding="utf-8"))
    for case in data["cases"]:
        if str(case.get("category", "")).lower() == "standard":
            return case
    return data["cases"][0]


def median_ms(samples: List[float]) -> float:
    return float(statistics.median(samples)) * 1000.0


def p95_ms(samples: List[float]) -> float:
    if not samples:
        return 0.0
    sorted_s = sorted(samples)
    # Index for 95th percentile, clamped to last index.
    idx = int(round(0.95 * (len(sorted_s) - 1)))
    return float(sorted_s[idx]) * 1000.0


def time_callable(fn: Callable[[], Any], reps: int = REPS) -> Dict[str, float]:
    samples: List[float] = []
    last: Any = None
    for _ in range(reps):
        t0 = perf_counter()
        last = fn()
        samples.append(perf_counter() - t0)
    return {
        "samples_sec": samples,
        "median_ms": median_ms(samples),
        "p95_ms": p95_ms(samples),
        "min_ms": min(samples) * 1000.0,
        "max_ms": max(samples) * 1000.0,
        "_last_result": last,
    }


def ollama_available_models(timeout_sec: float = 2.0) -> List[str] | None:
    """Return list of model names installed in Ollama, or None if unreachable."""
    try:
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            body = resp.read().decode("utf-8")
        data = json.loads(body)
        models = data.get("models", []) if isinstance(data, dict) else []
        return [str(m.get("name") or m.get("model") or "") for m in models if isinstance(m, dict)]
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, json.JSONDecodeError):
        return None


def pick_ollama_model() -> str | None:
    available = ollama_available_models()
    if available is None:
        return None
    available_set = set(available)
    for cand in OLLAMA_MODEL_CANDIDATES:
        if cand in available_set:
            return cand
    return None


def measure_per_discipline_evaluate() -> Dict[str, Any]:
    services = {
        "piping": PipingVerificationService(),
        "vessel": VesselVerificationService(),
        "rotating": RotatingVerificationService(),
        "electrical": ElectricalVerificationService(),
        "instrumentation": InstrumentationVerificationService(),
        "steel": SteelVerificationService(),
        "civil": CivilVerificationService(),
    }

    results: Dict[str, Any] = {}
    cached_results: Dict[str, Any] = {}
    for name, svc in services.items():
        case = first_standard_case(DATASETS[name])
        case_inputs = case["inputs"]
        timing = time_callable(lambda inp=case_inputs, s=svc: s.evaluate(inp))
        cached_results[name] = timing.pop("_last_result")
        results[name] = {
            "case_id": case.get("case_id"),
            "criticality": case.get("criticality"),
            **timing,
        }
    return {"per_discipline": results, "cached_results": cached_results}


def measure_piping_per_layer() -> Dict[str, Any]:
    """Per-layer timing for piping (the only service with cleanly separable internal layer methods)."""
    svc = PipingVerificationService()
    case = first_standard_case(DATASETS["piping"])
    payload = case["inputs"]

    # Pre-parse so we can call the internal layer methods directly.
    piping_input = parse_piping_input(payload)
    context, _refs, _issues = svc._lookup_standard_context(piping_input)  # noqa: SLF001
    candidates_for_l3l4 = svc._run_maker_candidates(piping_input, context)  # noqa: SLF001
    # Build a representative selected-candidate identical to runtime path.
    from src.piping.verification import build_layer2_consensus
    from src.piping.constants import CONSENSUS_REL_TOLERANCE

    _, selected = build_layer2_consensus(candidates_for_l3l4, tolerance=CONSENSUS_REL_TOLERANCE)

    layer_timings: Dict[str, Any] = {}

    layer1 = time_callable(lambda pi=piping_input, s=svc: s._run_layer1_input_validation(pi))  # noqa: SLF001
    layer1.pop("_last_result", None)
    layer_timings["layer1_input_validation"] = layer1

    # Layer 2 = K-voting: 3 candidate runs + consensus selection.
    def layer2_call() -> Any:
        cands = svc._run_maker_candidates(piping_input, context)  # noqa: SLF001
        _layer, sel = build_layer2_consensus(cands, tolerance=CONSENSUS_REL_TOLERANCE)
        return sel

    layer2 = time_callable(layer2_call)
    layer2.pop("_last_result", None)
    layer_timings["layer2_k_voting_3candidates_plus_consensus"] = layer2

    layer3 = time_callable(lambda pi=piping_input, sel=selected, s=svc: s._run_layer3_physics_and_standards(pi, sel))  # noqa: SLF001
    layer3.pop("_last_result", None)
    layer_timings["layer3_physics_and_standards"] = layer3

    layer4 = time_callable(lambda pi=piping_input, sel=selected, ctx=context, s=svc: s._run_layer4_reverse_checks(pi, sel, ctx))  # noqa: SLF001
    layer4.pop("_last_result", None)
    layer_timings["layer4_reverse_checks"] = layer4

    return {
        "case_id": case.get("case_id"),
        "layers": layer_timings,
    }


def measure_cross_discipline(cached_results: Dict[str, Any]) -> Dict[str, Any]:
    validator = CrossDisciplineValidator(thresholds=CrossDisciplineThresholds())

    payload = build_payload(
        p_res=cached_results["piping"],
        v_res=cached_results["vessel"],
        r_res=cached_results["rotating"],
        e_res=cached_results["electrical"],
        i_res=cached_results["instrumentation"],
        s_res=cached_results["steel"],
        c_res=cached_results["civil"],
    )
    timing = time_callable(lambda pl=payload, v=validator: v.evaluate(pl))
    timing.pop("_last_result", None)
    return timing


def measure_rag_retrieval() -> Dict[str, Any]:
    if not DEFAULT_INDEX_PATH.exists():
        raise RuntimeError(
            f"KOSHA RAG index not found at {DEFAULT_INDEX_PATH}. "
            "Build it with: python -m src.rag.local_kosha_rag build"
        )
    conn = connect_db(DEFAULT_INDEX_PATH)
    try:
        timing = time_callable(lambda c=conn: search_index(c, RAG_QUERY, RAG_TOPK, discipline="vessel"))
    finally:
        # Reopen for the result we need to keep.
        pass
    last_hits = timing.pop("_last_result")
    conn.close()
    return {"timing": timing, "hit_count": len(last_hits or []), "last_hits": last_hits}


def measure_rag_generation(hits: List[Any]) -> Dict[str, Any]:
    available = ollama_available_models()
    if available is None:
        return {
            "skipped": True,
            "reason": f"generation step skipped: Ollama not reachable on {OLLAMA_HOST}",
        }
    model = pick_ollama_model()
    if model is None:
        return {
            "skipped": True,
            "reason": (
                f"generation step skipped: none of the candidate Qwen models are installed "
                f"in Ollama. Candidates={list(OLLAMA_MODEL_CANDIDATES)}, available={available}"
            ),
        }

    prompt = build_prompt(RAG_QUERY, hits[:5])

    def gen_once() -> str:
        return generate_with_ollama(OLLAMA_GEN_URL, model, prompt)

    try:
        timing = time_callable(gen_once, reps=REPS)
    except RuntimeError as exc:
        return {
            "skipped": True,
            "reason": f"generation step skipped: Ollama call failed: {exc}",
        }
    timing.pop("_last_result", None)
    return {"skipped": False, "model": model, "prompt_chars": len(prompt), **timing}


def header_info() -> Dict[str, Any]:
    return {
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "python_version": sys.version.split()[0],
        "cpu_processor": platform.processor() or "unknown",
        "machine": platform.machine(),
        "reps_per_stage": REPS,
    }


def end_to_end_median(per_discipline: Dict[str, Any], cross_disc_ms: float, rag_ret_ms: float, rag_gen_ms: float | None) -> float:
    """Compose a representative end-to-end median = piping evaluate + cross-disc + RAG retrieval + RAG generation."""
    base = float(per_discipline["piping"]["median_ms"]) + float(cross_disc_ms) + float(rag_ret_ms)
    if rag_gen_ms is not None:
        base += float(rag_gen_ms)
    return base


def run() -> Dict[str, Any]:
    info = header_info()
    per_disc = measure_per_discipline_evaluate()
    cached = per_disc.pop("cached_results")
    piping_layers = measure_piping_per_layer()
    cross_disc = measure_cross_discipline(cached)
    rag_ret = measure_rag_retrieval()
    rag_gen = measure_rag_generation(rag_ret["last_hits"])

    rag_ret_clean = {k: v for k, v in rag_ret["timing"].items()}
    rag_ret_payload = {
        "query": RAG_QUERY,
        "top_k": RAG_TOPK,
        "hit_count": rag_ret["hit_count"],
        **rag_ret_clean,
    }

    e2e_median_ms = end_to_end_median(
        per_disc["per_discipline"],
        cross_disc["median_ms"],
        rag_ret_payload["median_ms"],
        None if rag_gen.get("skipped") else rag_gen.get("median_ms"),
    )

    return {
        "header": info,
        "per_discipline_evaluate": per_disc["per_discipline"],
        "piping_per_layer": piping_layers,
        "cross_discipline_validator": cross_disc,
        "rag_retrieval": rag_ret_payload,
        "rag_generation": rag_gen,
        "end_to_end_median_ms": e2e_median_ms,
    }


def write_reports(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    # Drop non-serializable objects from per-stage records.
    sanitized = json.loads(json.dumps(report, default=lambda o: str(o), ensure_ascii=False))
    OUT_JSON.write_text(json.dumps(sanitized, indent=2, ensure_ascii=False), encoding="utf-8")

    h = report["header"]
    lines = [
        "# Pipeline End-to-End Latency Report",
        "",
        f"- Platform: {h['platform_system']} {h['platform_release']} ({h['machine']})",
        f"- Python: {h['python_version']}",
        f"- CPU: {h['cpu_processor']}",
        f"- Repetitions per stage: {h['reps_per_stage']} (median + p95 reported)",
        "",
        "## Per-Discipline Layered Stack (Layers 1-4 Combined, service.evaluate)",
        "",
        "| Discipline | Case ID | Criticality | Median (ms) | p95 (ms) | Min (ms) | Max (ms) |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for name in ("piping", "vessel", "rotating", "electrical", "instrumentation", "steel", "civil"):
        r = report["per_discipline_evaluate"][name]
        lines.append(
            f"| {name} | {r['case_id']} | {r['criticality']} | "
            f"{r['median_ms']:.2f} | {r['p95_ms']:.2f} | {r['min_ms']:.2f} | {r['max_ms']:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Piping Per-Layer Breakdown",
            f"_Case: {report['piping_per_layer']['case_id']}_",
            "",
            "| Layer | Median (ms) | p95 (ms) | Min (ms) | Max (ms) |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for layer_name, t in report["piping_per_layer"]["layers"].items():
        lines.append(
            f"| {layer_name} | {t['median_ms']:.3f} | {t['p95_ms']:.3f} | "
            f"{t['min_ms']:.3f} | {t['max_ms']:.3f} |"
        )

    cd = report["cross_discipline_validator"]
    lines.extend(
        [
            "",
            "## Cross-Discipline Validator (One Paired Call Across 7 Disciplines)",
            "",
            f"- Median: {cd['median_ms']:.3f} ms",
            f"- p95: {cd['p95_ms']:.3f} ms",
            f"- Min/Max: {cd['min_ms']:.3f} / {cd['max_ms']:.3f} ms",
        ]
    )

    rr = report["rag_retrieval"]
    lines.extend(
        [
            "",
            "## KOSHA RAG Retrieval (top-10)",
            "",
            f"- Query: `{rr['query']}`",
            f"- Hit count: {rr['hit_count']}",
            f"- Median: {rr['median_ms']:.3f} ms",
            f"- p95: {rr['p95_ms']:.3f} ms",
            f"- Min/Max: {rr['min_ms']:.3f} / {rr['max_ms']:.3f} ms",
        ]
    )

    rg = report["rag_generation"]
    lines.extend(["", "## KOSHA RAG Generation (Qwen via Ollama)", ""])
    if rg.get("skipped"):
        lines.append(f"- Status: skipped")
        lines.append(f"- Reason: {rg.get('reason', 'unknown')}")
    else:
        lines.append(f"- Model: {rg['model']}")
        lines.append(f"- Prompt chars: {rg['prompt_chars']}")
        lines.append(f"- Median: {rg['median_ms']:.1f} ms")
        lines.append(f"- p95: {rg['p95_ms']:.1f} ms")
        lines.append(f"- Min/Max: {rg['min_ms']:.1f} / {rg['max_ms']:.1f} ms")

    lines.extend(
        [
            "",
            "## End-to-End Median",
            "",
            "Composition: piping `service.evaluate` median + cross-discipline validator median + RAG retrieval median ("
            + ("+ RAG generation median" if not rg.get("skipped") else "RAG generation skipped")
            + ").",
            "",
            f"- End-to-end median: {report['end_to_end_median_ms']:.2f} ms",
        ]
    )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = run()
    write_reports(report)
    print(f"REPORT_JSON={OUT_JSON}")
    print(f"REPORT_MD={OUT_MD}")
    print(f"END_TO_END_MEDIAN_MS={report['end_to_end_median_ms']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
