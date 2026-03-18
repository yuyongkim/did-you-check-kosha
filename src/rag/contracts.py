from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class StandardSearchQuery:
    query: str
    discipline: str | None = None
    filters: Dict[str, object] | None = None


@dataclass
class Citation:
    standard: str
    section_or_table: str
    page: int
    version: str


@dataclass
class StandardSearchResult:
    content: str
    score: float
    citations: List[Citation]
    conditions: List[str]
