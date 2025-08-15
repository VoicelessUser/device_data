from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class PowerSupplyChannel:
    number: int
    name: str
    volt: float
    max_current: float
    is_enabled: bool
    is_readable: bool
    max_rating: Optional[float] = None
    typical_rating: Optional[float] = None

@dataclass
class PowerSupply:
    channels: List[PowerSupplyChannel] = field(default_factory=lambda: [
        PowerSupplyChannel(1, '', 5.0, 0.01, True, True),
        PowerSupplyChannel(2, '', 5.0, 0.01, True, False),
        PowerSupplyChannel(3, '', 5.0, 0.01, False, False)
    ])
