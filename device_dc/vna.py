from dataclasses import dataclass, field
from typing import Optional

@dataclass
class VNA:
    power: float = 0.0
    max_freq: float = 10e9
    targ_freq: dict[float, dict[str, Optional[float]]] = field(default_factory=dict)
    TRACE_NAME: dict[str, str] = field(default_factory=lambda: {
        'S11': 'S11',
        'S12': 'S12',
        'S21': 'S21',
        'S22': 'S22'
    })