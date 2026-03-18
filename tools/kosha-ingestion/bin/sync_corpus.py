#!/usr/bin/env python3
"""CLI wrapper for kosha_ingestion.sync_corpus."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
  sys.path.insert(0, str(SRC))

from kosha_ingestion.sync_corpus import main


if __name__ == "__main__":
  raise SystemExit(main())
