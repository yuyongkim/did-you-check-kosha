"""Generate the five publication figures for JLP-D-26-00414 revision.

Single entry point — run with:
    python scripts/generate_paper_figures.py

All figures written to docs/publication/figures/ as 200-DPI PNGs.

Numerical content is read from existing repo artifacts:
- src/cross_discipline/validator.py             -> Figure 3 edges
- outputs/cross_discipline_ablation_report.json -> Figure 4 bars
- outputs/rag_retrieval_report.md               -> Figure 5 bars
- datasets/kosha_rag/README.md                  -> Figure 1/2 corpus counts
- datasets/kosha/manifest.json                  -> Figure 1/2 cross-check

This script intentionally relies only on matplotlib (already a dep) plus the
Python standard library — no networkx, no graphviz, no seaborn.
"""

from __future__ import annotations

import ast
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_ROOT / "docs" / "publication" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

VALIDATOR_PY = REPO_ROOT / "src" / "cross_discipline" / "validator.py"
ABLATION_JSON = REPO_ROOT / "outputs" / "cross_discipline_ablation_report.json"
RAG_REPORT_MD = REPO_ROOT / "outputs" / "rag_retrieval_report.md"
KOSHA_RAG_README = REPO_ROOT / "datasets" / "kosha_rag" / "README.md"
KOSHA_MANIFEST = REPO_ROOT / "datasets" / "kosha" / "manifest.json"

DPI = 200

# ----------------------------------------------------------------------------
# Print-safe palette (avoid neon)
# ----------------------------------------------------------------------------
COLOR_INPUT = "#4F6D7A"
COLOR_ENGINE = "#86A5B0"
COLOR_VERIFY = "#B07C56"
COLOR_COUPLING = "#7C8C5C"
COLOR_RAG = "#5C6B8C"
COLOR_OUTPUT = "#3D4A5C"
COLOR_ARROW = "#2E2E2E"
COLOR_TEXT = "#1A1A1A"
COLOR_OFF = "#A6A6A6"
COLOR_ON = "#4F6D7A"
COLOR_PLAIN = "#A6A6A6"
COLOR_ENH = "#7C8C5C"
COLOR_NODE = "#4F6D7A"
COLOR_EDGE = "#7A6E5C"

MISSING_INPUTS: list[str] = []


# ----------------------------------------------------------------------------
# Helper readers
# ----------------------------------------------------------------------------
def read_check_pairs() -> list[tuple[str, str, str]]:
    """Parse the _CHECK_PAIRS literal from the validator module without executing it."""
    if not VALIDATOR_PY.exists():
        MISSING_INPUTS.append(str(VALIDATOR_PY))
        return []
    src = VALIDATOR_PY.read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "_CHECK_PAIRS":
                    if isinstance(node.value, (ast.List, ast.Tuple)):
                        return [tuple(ast.literal_eval(elt)) for elt in node.value.elts]
    return []


def read_ablation() -> dict[str, Any]:
    if not ABLATION_JSON.exists():
        MISSING_INPUTS.append(str(ABLATION_JSON))
        return {}
    return json.loads(ABLATION_JSON.read_text(encoding="utf-8"))


def read_rag_report() -> dict[str, Any]:
    """Parse the RAG retrieval markdown report into a structured dict."""
    if not RAG_REPORT_MD.exists():
        MISSING_INPUTS.append(str(RAG_REPORT_MD))
        return {}
    text = RAG_REPORT_MD.read_text(encoding="utf-8")
    out: dict[str, Any] = {"groups": [], "overall": {}}

    # Overall metrics
    plain_match = re.search(
        r"Plain FTS:\s*Recall@1=([\d.]+),\s*Recall@3=([\d.]+),\s*Recall@5=([\d.]+),\s*MRR@10=([\d.]+)",
        text,
    )
    enh_match = re.search(
        r"Enhanced FTS:\s*Recall@1=([\d.]+),\s*Recall@3=([\d.]+),\s*Recall@5=([\d.]+),\s*MRR@10=([\d.]+)",
        text,
    )
    if plain_match and enh_match:
        out["overall"] = {
            "plain": {
                "r1": float(plain_match.group(1)),
                "r3": float(plain_match.group(2)),
                "r5": float(plain_match.group(3)),
                "mrr10": float(plain_match.group(4)),
            },
            "enhanced": {
                "r1": float(enh_match.group(1)),
                "r3": float(enh_match.group(2)),
                "r5": float(enh_match.group(3)),
                "mrr10": float(enh_match.group(4)),
            },
        }

    # Per-group lines: "- <name>: Plain R@5=0.9000, Enhanced R@5=1.0000, delta=0.1000"
    for m in re.finditer(
        r"-\s*(.+?):\s*Plain R@5=([\d.]+),\s*Enhanced R@5=([\d.]+),\s*delta=([-\d.]+)",
        text,
    ):
        out["groups"].append(
            {
                "name": m.group(1).strip(),
                "plain": float(m.group(2)),
                "enhanced": float(m.group(3)),
                "delta": float(m.group(4)),
            }
        )
    return out


def read_kosha_counts() -> dict[str, int]:
    """Pull the indexed-corpus counts from the kosha_rag README."""
    counts = {"guide_chunks": 13084, "law_articles": 3090, "total_indexed": 16174}
    if not KOSHA_RAG_README.exists():
        MISSING_INPUTS.append(str(KOSHA_RAG_README))
        return counts
    text = KOSHA_RAG_README.read_text(encoding="utf-8")
    m = re.search(r"guide chunks indexed:\s*`([\d,]+)`", text)
    if m:
        counts["guide_chunks"] = int(m.group(1).replace(",", ""))
    m = re.search(r"indexed law-article entries:\s*`([\d,]+)`", text)
    if m:
        counts["law_articles"] = int(m.group(1).replace(",", ""))
    m = re.search(r"total indexed searchable documents:\s*`([\d,]+)`", text)
    if m:
        counts["total_indexed"] = int(m.group(1).replace(",", ""))
    return counts


# ----------------------------------------------------------------------------
# Drawing primitives
# ----------------------------------------------------------------------------
def add_box(ax, x, y, w, h, text, face, *, fontsize=10, edge="#222", lw=1.2, text_color="white"):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        linewidth=lw,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=text_color,
        wrap=True,
    )


def add_arrow(ax, x1, y1, x2, y2, *, color=COLOR_ARROW, lw=1.5, style="-|>", mut=14):
    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle=style,
        mutation_scale=mut,
        linewidth=lw,
        color=color,
        shrinkA=2,
        shrinkB=2,
    )
    ax.add_patch(arrow)


# ----------------------------------------------------------------------------
# Figure 1 — System architecture (horizontal block diagram)
# ----------------------------------------------------------------------------
def fig_1_system_architecture(out_path: Path) -> None:
    counts = read_kosha_counts()

    fig, ax = plt.subplots(figsize=(16, 7), dpi=DPI)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title(
        "Figure 1. End-to-end system architecture: discipline engines, hybrid verification,\n"
        "cross-discipline coupling, and KOSHA regulatory RAG",
        fontsize=13,
        pad=14,
    )

    # Input
    add_box(ax, 0.2, 2.8, 1.8, 1.4, "Input\nDiscipline-specific\ncalculation request", COLOR_INPUT, fontsize=9)

    # Box 1: Seven engines
    engines_text = (
        "Seven domain calculation engines\n"
        "Piping  |  Static Equipment  |  Rotating\n"
        "Electrical  |  Instrumentation  |  Steel  |  Civil"
    )
    add_box(ax, 2.4, 2.6, 3.4, 1.8, engines_text, COLOR_ENGINE, fontsize=9, text_color="#1a1a1a")

    # Box 2: Four-layer hybrid verification
    verify_text = (
        "Four-layer hybrid verification\n"
        "L1  Input validation\n"
        "L2  K-voting (3 paths, 1% tol.)\n"
        "L3  Invariant check\n"
        "L4  Reverse verify (2% warn / 5% esc.)"
    )
    add_box(ax, 6.2, 2.4, 3.2, 2.2, verify_text, COLOR_VERIFY, fontsize=9)

    # Box 3: Cross-discipline coupling
    coupling_text = (
        "Cross-discipline\ncoupling validator\n10 predefined pairs\n(piping vessel rotating\nelectrical instrumentation\nsteel civil)"
    )
    add_box(ax, 9.8, 4.2, 2.6, 2.2, coupling_text, COLOR_COUPLING, fontsize=9)

    # Box 4: KOSHA RAG
    rag_text = (
        f"KOSHA Regulatory RAG\n"
        f"{counts['total_indexed']:,} indexed rows\n"
        f"{counts['guide_chunks']:,} guide chunks\n"
        f"+ {counts['law_articles']:,} law articles\n"
        f"Concept-aware synonym\nexpansion + SQLite FTS5"
    )
    add_box(ax, 9.8, 0.7, 2.6, 2.6, rag_text, COLOR_RAG, fontsize=9)

    # Output
    output_text = (
        "Output\nStructured engineering\nverdict + regulatory\ncitations"
    )
    add_box(ax, 13.0, 2.6, 2.7, 1.8, output_text, COLOR_OUTPUT, fontsize=9)

    # Arrows: Input -> Engines -> Verify -> (Coupling | RAG) -> Output
    add_arrow(ax, 2.0, 3.5, 2.4, 3.5)
    add_arrow(ax, 5.8, 3.5, 6.2, 3.5)
    add_arrow(ax, 9.4, 3.7, 9.8, 4.7)   # Verify -> Coupling
    add_arrow(ax, 9.4, 3.1, 9.8, 2.2)   # Verify -> RAG
    add_arrow(ax, 12.4, 5.0, 13.0, 4.0)  # Coupling -> Output
    add_arrow(ax, 12.4, 1.9, 13.0, 3.0)  # RAG -> Output

    # Footer caption
    ax.text(
        8.0,
        0.15,
        "All on-prem inference (Qwen 2.5 7B Instruct via Ollama). No external transmission of plant data.",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#444",
        style="italic",
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Figure 2 — RAG workflow (vertical flow)
# ----------------------------------------------------------------------------
def fig_2_rag_workflow(out_path: Path) -> None:
    counts = read_kosha_counts()
    fig, ax = plt.subplots(figsize=(9, 12), dpi=DPI)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.set_title(
        "Figure 2. KOSHA Regulatory RAG workflow — query to grounded answer",
        fontsize=12,
        pad=14,
    )

    steps = [
        ("1. User query\n(Korean or English engineering term)", COLOR_INPUT),
        ("2. Concept-aware query builder\n(engineering_synonyms expansion -> OR fallback)", COLOR_ENGINE),
        (
            f"3. SQLite FTS5 over {counts['total_indexed']:,} indexed documents\n"
            f"({counts['guide_chunks']:,} guide chunks + {counts['law_articles']:,} law articles)",
            COLOR_VERIFY,
        ),
        ("4. Top-K candidate hits (deduped)", COLOR_COUPLING),
        ("5. Discipline-aware filter", COLOR_RAG),
        (
            "6. Local Qwen 2.5 7B Instruct via on-prem Ollama\n(no external transmission of plant data)",
            COLOR_OUTPUT,
        ),
        (
            "7. Grounded answer with reference codes\ne.g.  M-69-2012   |   Article 256 (corrosion prevention)",
            COLOR_INPUT,
        ),
    ]

    box_w = 6.4
    box_h = 1.15
    x = (9 - box_w) / 2
    top = 11.0
    gap = 0.45
    centers_y = []
    for i, (text, face) in enumerate(steps):
        y = top - i * (box_h + gap)
        centers_y.append(y + box_h / 2)
        add_box(ax, x, y, box_w, box_h, text, face, fontsize=10)

    # Vertical arrows between consecutive steps
    for i in range(len(steps) - 1):
        y_from = centers_y[i] - box_h / 2 - 0.02
        y_to = centers_y[i + 1] + box_h / 2 + 0.02
        add_arrow(ax, 4.5, y_from, 4.5, y_to, lw=1.6)

    fig.tight_layout()
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Figure 3 — Cross-discipline coupling logic (circular graph)
# ----------------------------------------------------------------------------
def fig_3_cross_discipline(out_path: Path) -> None:
    pairs = read_check_pairs()
    disciplines = ["piping", "vessel", "rotating", "electrical", "instrumentation", "steel", "civil"]

    # Position 7 disciplines on a circle
    n = len(disciplines)
    radius = 3.4
    cx, cy = 5.0, 5.0
    coords: dict[str, tuple[float, float]] = {}
    for i, d in enumerate(disciplines):
        angle = math.pi / 2 - i * (2 * math.pi / n)
        coords[d] = (cx + radius * math.cos(angle), cy + radius * math.sin(angle))

    fig, ax = plt.subplots(figsize=(11, 10), dpi=DPI)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title(
        f"Figure 3. Cross-discipline coupling validator: {len(pairs)} predefined discipline pairs",
        fontsize=12,
        pad=14,
    )

    # Edges first (so nodes draw on top)
    label_offsets: list[tuple[float, float, str]] = []
    for a, b, method in pairs:
        if a not in coords or b not in coords:
            continue
        xa, ya = coords[a]
        xb, yb = coords[b]
        ax.plot([xa, xb], [ya, yb], color=COLOR_EDGE, linewidth=1.4, alpha=0.85, zorder=1)
        # Edge label = check method without leading underscore and "_check_" prefix
        label = method.lstrip("_")
        if label.startswith("check_"):
            label = label[len("check_") :]
        # Slight offset perpendicular to the line for legibility
        mx, my = (xa + xb) / 2, (ya + yb) / 2
        dx, dy = xb - xa, yb - ya
        norm = math.hypot(dx, dy) or 1.0
        # perpendicular unit vector
        px, py = -dy / norm, dx / norm
        label_offsets.append((mx + px * 0.18, my + py * 0.18, label))

    for x, y, text in label_offsets:
        ax.text(
            x,
            y,
            text,
            ha="center",
            va="center",
            fontsize=7,
            color="#333",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="#bbb", linewidth=0.6, alpha=0.92),
            zorder=2,
        )

    # Nodes
    node_r = 0.55
    for d, (x, y) in coords.items():
        circle = patches.Circle((x, y), node_r, facecolor=COLOR_NODE, edgecolor="#222", linewidth=1.4, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, d.capitalize(), ha="center", va="center", fontsize=9, color="white", weight="bold", zorder=4)

    ax.text(
        5.0,
        0.4,
        f"Source: src/cross_discipline/validator.py  |  {len(pairs)} pairs trigger physically motivated coupling checks at run time.",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#444",
        style="italic",
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Figure 4 — Ablation bar chart
# ----------------------------------------------------------------------------
def fig_4_ablation(out_path: Path) -> None:
    data = read_ablation()
    if not data:
        return
    sets = data.get("scenario_sets", [])
    labels = []
    off_vals = []
    on_vals = []
    for s in sets:
        labels.append(s["set_name"].replace("aligned_", "").replace("_", " "))
        off_vals.append(int(s["validator_off"]["blocked_scenarios"]))
        on_vals.append(int(s["validator_on"]["blocked_scenarios"]))

    # Append totals
    labels.append("total")
    off_vals.append(int(data.get("validator_off", {}).get("blocked_scenarios", 0)))
    on_vals.append(int(data.get("validator_on", {}).get("blocked_scenarios", 0)))

    total = data.get("total_scenarios", sum(s["total_scenarios"] for s in sets) if sets else 0)
    on_blocked = data.get("validator_on", {}).get("blocked_scenarios", 0)
    pct = (on_blocked / total * 100) if total else 0.0

    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=DPI)
    x = list(range(len(labels)))
    width = 0.36
    bars_off = ax.bar([i - width / 2 for i in x], off_vals, width, color=COLOR_OFF, label="Cross-discipline OFF", edgecolor="#444")
    bars_on = ax.bar([i + width / 2 for i in x], on_vals, width, color=COLOR_ON, label="Cross-discipline ON", edgecolor="#222")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0, fontsize=9)
    ax.set_ylabel("Blocked scenarios (count)", fontsize=10)
    ax.set_title(
        f"Figure 4. Cross-discipline ablation: 0 -> {on_blocked} scenarios blocked (+{pct:.1f}%)",
        fontsize=12,
        pad=12,
    )
    ax.set_ylim(0, max(on_vals + off_vals) * 1.25 + 1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.45)
    ax.legend(loc="upper left", frameon=False)

    for bar in list(bars_off) + list(bars_on):
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.15,
            f"{int(h)}",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#222",
        )

    ax.text(
        0.99,
        -0.14,
        f"Source: outputs/cross_discipline_ablation_report.json  |  N={total} scenarios",
        ha="right",
        va="top",
        transform=ax.transAxes,
        fontsize=8,
        color="#666",
        style="italic",
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Figure 5 — Per-group Recall@5 + overall Recall@1 / MRR@10
# ----------------------------------------------------------------------------
def fig_5_retrieval_metrics(out_path: Path) -> None:
    rep = read_rag_report()
    if not rep or not rep.get("groups"):
        return
    groups = rep["groups"]
    overall = rep.get("overall", {})

    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5), dpi=DPI, gridspec_kw={"width_ratios": [2.0, 1.0]})
    ax1, ax2 = axes

    # ---- Left: per-group Recall@5 ----
    labels = [g["name"] for g in groups]
    plain = [g["plain"] for g in groups]
    enh = [g["enhanced"] for g in groups]
    deltas = [g["delta"] for g in groups]
    x = list(range(len(labels)))
    width = 0.36
    bars_p = ax1.bar([i - width / 2 for i in x], plain, width, color=COLOR_PLAIN, label="Plain FTS", edgecolor="#444")
    bars_e = ax1.bar([i + width / 2 for i in x], enh, width, color=COLOR_ENH, label="Enhanced FTS", edgecolor="#222")
    ax1.set_xticks(x)
    ax1.set_xticklabels([_wrap_label(label) for label in labels], fontsize=8)
    ax1.set_ylim(0, 1.15)
    ax1.set_ylabel("Recall@5", fontsize=10)
    ax1.set_title("(a) Per-group Recall@5: Plain vs Enhanced FTS", fontsize=11)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="y", linestyle=":", alpha=0.45)
    ax1.legend(loc="lower right", frameon=False)

    for bar in list(bars_p) + list(bars_e):
        h = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.015,
            f"{h:.2f}",
            ha="center",
            va="bottom",
            fontsize=8,
            color="#222",
        )

    # Delta annotations between bar pairs
    for i, d in enumerate(deltas):
        sign = "+" if d > 0 else ""
        color = "#1f6f3a" if d > 0 else "#666"
        ymax = max(plain[i], enh[i]) + 0.10
        ax1.text(i, ymax, f"d={sign}{d:.2f}", ha="center", va="bottom", fontsize=8, color=color, weight="bold")

    # ---- Right: overall Recall@1 and MRR@10 ----
    if overall:
        metric_names = ["Recall@1", "MRR@10"]
        plain_vals = [overall["plain"]["r1"], overall["plain"]["mrr10"]]
        enh_vals = [overall["enhanced"]["r1"], overall["enhanced"]["mrr10"]]
        x2 = list(range(len(metric_names)))
        bp = ax2.bar([i - width / 2 for i in x2], plain_vals, width, color=COLOR_PLAIN, label="Plain FTS", edgecolor="#444")
        be = ax2.bar([i + width / 2 for i in x2], enh_vals, width, color=COLOR_ENH, label="Enhanced FTS", edgecolor="#222")
        ax2.set_xticks(x2)
        ax2.set_xticklabels(metric_names, fontsize=10)
        ax2.set_ylim(0, 1.05)
        ax2.set_ylabel("Score", fontsize=10)
        ax2.set_title("(b) Overall Recall@1 and MRR@10", fontsize=11)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.grid(axis="y", linestyle=":", alpha=0.45)
        ax2.legend(loc="lower right", frameon=False)
        for bar in list(bp) + list(be):
            h = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                h + 0.015,
                f"{h:.3f}",
                ha="center",
                va="bottom",
                fontsize=9,
                color="#222",
            )

    fig.suptitle(
        "Figure 5. Concept-aware query expansion lifts retrieval across all five regulatory groups",
        fontsize=12,
        y=1.02,
    )
    fig.text(
        0.5,
        -0.02,
        "Source: outputs/rag_retrieval_report.md  |  5 groups x 10 queries = 50 total benchmark queries",
        ha="center",
        va="top",
        fontsize=8,
        color="#666",
        style="italic",
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _wrap_label(label: str, width: int = 18) -> str:
    """Soft-wrap a long group label across two lines on whitespace."""
    if len(label) <= width:
        return label
    words = label.split()
    line1, line2 = "", ""
    for w in words:
        if len(line1) + len(w) + 1 <= width:
            line1 = (line1 + " " + w).strip()
        else:
            line2 = (line2 + " " + w).strip()
    return f"{line1}\n{line2}".strip()


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main() -> int:
    targets = [
        ("fig_1_system_architecture.png", fig_1_system_architecture),
        ("fig_2_rag_workflow.png", fig_2_rag_workflow),
        ("fig_3_cross_discipline.png", fig_3_cross_discipline),
        ("fig_4_ablation.png", fig_4_ablation),
        ("fig_5_retrieval_metrics.png", fig_5_retrieval_metrics),
    ]
    produced: list[tuple[Path, int]] = []
    for fname, fn in targets:
        out_path = FIG_DIR / fname
        fn(out_path)
        if out_path.exists():
            produced.append((out_path, out_path.stat().st_size))
        else:
            print(f"[WARN] Figure not produced: {out_path}", file=sys.stderr)

    print("Generated figures:")
    for p, sz in produced:
        print(f"  {p}  ({sz:,} bytes)")
    if MISSING_INPUTS:
        print("\nMissing or unreadable inputs:")
        for m in MISSING_INPUTS:
            print(f"  {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
