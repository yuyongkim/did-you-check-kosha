from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SpecialistTask:
    discipline: str
    calculation_type: str
    input_data: Dict[str, object]
    standards_context: List[Dict[str, object]]
