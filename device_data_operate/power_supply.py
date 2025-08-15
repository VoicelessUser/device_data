from dataclasses import asdict

from device_dc import PowerSupply



class PowerSupplyDO:
    def __init__(self):
        self.data = PowerSupply()

    def test_channel_max(self, read_current: list[float]) -> list[bool | None]:
        more_then_max: list[bool | None] = []
        for ch, read_curr in zip(self.data.channels, read_current):
            if ch.is_readable and read_curr and ch.is_enabled:
                more_then_max.append(ch.max_rating <= read_curr)
            else:
                more_then_max.append(None)
        return more_then_max

    def test_channel_typ(self, read_current: list[float])-> list[bool | None]:
        more_than_typ: list[bool | None] = []
        for ch, read_curr in zip(self.data.channels, read_current):
            if ch.is_readable and read_curr and ch.is_enabled:
                more_than_typ.append(ch.typical_rating <= read_curr)
            else:
                more_than_typ.append(None)
        return more_than_typ

    def clear(self) -> None:
        for ch in self.data.channels:
            ch.max_rating = None
            ch.typical_rating = None

    def create_conditions(self)-> str:
        return ', '.join(
            f'V{ch.name} = {ch.volt} В'
            for ch in self.data.channels
            if ch.name
        )

    def create_datasheet(self) -> str:
        """Формирует спецификацию по токам"""
        specs = []
        for ch in filter(lambda c: c.read, self.data.channels):
            if ch.datasheet_max:
                specs.append(f'ток I{ch.name} должен быть меньше {ch.max_rating * 1000} мА')
            if ch.datasheet_typ:
                specs.append(f'типовое значение I{ch.name} = {ch.typical_rating * 1000} мА')
        return ', '.join(specs)

    def shift_to_dict(self)-> dict[str, dict]:
        return {
            'power_supply': asdict(self.data)
        }

    def from_dict_to_data(self, data_dict: dict[str, dict]) -> None:
        """Обновляет данные из словаря, используя автоматическое преобразование."""
        power_supply_data = data_dict.get('power_supply')
        if not power_supply_data:
            return

        for ch_data in power_supply_data.get('channels', []):
            channel = next(
                (ch for ch in self.data.channels if ch.number == ch_data.get('number')),
                None
            )
            if channel:
                # Конвертируем dataclass в словарь, обновляем и исключаем 'number'
                channel_dict = asdict(channel)
                channel_dict.update({k: v for k, v in ch_data.items() if k != 'number'})

                # Обновляем поля channel (без замены самого объекта)
                for key, value in channel_dict.items():
                    setattr(channel, key, value)