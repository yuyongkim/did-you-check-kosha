#!/usr/bin/env python3
"""Run local KOSHA RAG (SQLite FTS + optional Ollama generation)."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

from src.rag.local_kosha_rag import main


if __name__ == "__main__":
  raise SystemExit(main())
