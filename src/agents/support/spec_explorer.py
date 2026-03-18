from __future__ import annotations

from typing import Dict, List, Protocol


class SpecExplorer(Protocol):
    def search_standard(self, query: str, discipline: str | None = None, filters: Dict[str, object] | None = None) -> List[Dict[str, object]]:
        ...

    def extract_table_value(self, standard: str, table: str, lookup_conditions: Dict[str, object]) -> Dict[str, object]:
        ...
