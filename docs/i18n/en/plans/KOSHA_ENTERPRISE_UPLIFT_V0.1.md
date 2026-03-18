# KOSHA Enterprise Uplift Plan V0.1 (EN)

## 1. Problem Statement

The current product has strong engineering logic but can still look like a generic calculator if regulatory evidence is not shown at the point of decision.

Enterprise users in EPC do not primarily buy visual polish. They buy:
- calculation credibility,
- standards and legal traceability,
- audit-ready outputs.

## 2. Strategic Principle

Design direction: `Industrial Modernism`.

Rules:
- maximize information density,
- prioritize trust signals over visual effects,
- keep layout stable and compact for real engineering work.

Target UI structure:
- Left 25%: input and context,
- Center 50%: calculations and trends,
- Right 25%: verification, KOSHA guides, legal mapping, compliance status.

## 3. KOSHA API Differentiation

Two approved API domains are combined:
- KOSHA Guide references: "how to design/inspect",
- Legal smart search: "why it is mandatory and what compliance risk exists".

Expected output shift:
- Before: numeric result only.
- After: numeric result + guide evidence + legal basis + compliance summary.

## 4. Execution Phases

### Phase 1 (Current sprint)
- Implement 3-pane dense layout.
- Integrate KOSHA guide + legal APIs.
- Render right-pane regulatory context with clear status badges.

### Phase 2 (Next sprint)
- Improve matching rules by discipline and risk signals.
- Add caching hardening and fault-tolerant fallback behavior.
- Extend export templates for audit submission.

### Phase 3
- Add retrieval-quality metrics and hit-rate dashboard.
- Add account-level policy profiles (owner/operator/inspector views).

## 5. KPI

- `Guide mapping coverage`: at least 2 references per calculation (where available).
- `Legal mapping precision`: at least 80% useful article hits in expert review.
- `Audit readiness`: one-click output with formula + standard + legal trace.
- `Response latency`: acceptable UI experience with caching enabled.

## 6. Technical Guardrails

- Keep `frontend/lib/kosha-regulatory.ts` as orchestration only.
- Move parsing/querying/mapping/compliance logic into `frontend/lib/kosha/*` modules.
- Preserve fallback behavior when API key, endpoint, or response fails.
- Always keep `.env`-based key management and do not hardcode secrets.

## 7. Immediate Action List

1. Maintain snapshot backups per major refactor.
2. Keep regulatory module boundaries clean and testable.
3. Keep right pane dense, explicit, and audit-oriented.
4. Avoid decorative UI work that does not improve trust or compliance speed.
