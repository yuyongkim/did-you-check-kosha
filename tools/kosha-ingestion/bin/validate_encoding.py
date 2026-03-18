#!/usr/bin/env python3
"""CLI entry for KOSHA snapshot encoding validation/repair."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "tools" / "kosha-ingestion" / "src"
if str(SRC) not in sys.path:
  sys.path.insert(0, str(SRC))

from kosha_ingestion.validate_encoding import main


if __name__ == "__main__":
  raise SystemExit(main())
