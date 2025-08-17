from dataclasses import dataclass, field

@dataclass
class BluePill:
    num_of_bits: int = 5
    inversion: bool = True
    type_inter_spi: bool = True
    delay: float = 0.1
    ALL_PINS: set[int] = field(default_factory=set)

    def __post_init__(self):
        self.ALL_PINS = {i + 1 for i in range(8)}



