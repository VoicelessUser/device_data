from dataclasses import asdict, is_dataclass

class DataOperate:
    TYPE_OF_DEVICE: str = ""  # Подклассы должны переопределить

    def __init__(self,dataclass_obj):
        if not is_dataclass(dataclass_obj):
            raise TypeError("Expected dataclass instance")
        self.value = dataclass_obj

    def __post_init__(self):
        if not self.TYPE_OF_DEVICE:
            raise ValueError("TYPE_OF_DEVICE must be set")

    def to_dict(self) -> dict:
        return {self.TYPE_OF_DEVICE: asdict(self.value)}

    def update_from_dict(self, data: dict) -> None:
        device_data = data.get(self.TYPE_OF_DEVICE)
        if not device_data:
            raise KeyError(f"Missing key: {self.TYPE_OF_DEVICE}")
        for key, value in device_data.items():
            if hasattr(self.value, key):
                setattr(self.value, key, value)