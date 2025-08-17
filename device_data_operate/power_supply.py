from data_operate import DataOperate
from device_dc import PowerSupply, PowerSupplyChannel


class PowerSupplyDO(DataOperate):
    TYPE_OF_DEVICE = 'power_supply'

    def __init__(self, power_supply: PowerSupply = None):
        if power_supply is None:
            power_supply = PowerSupply()
        super().__init__(power_supply)

    def update_from_dict(self, data: dict) -> None:
        """Переопределяем метод для правильной загрузки вложенных объектов"""
        device_data = data.get(self.TYPE_OF_DEVICE)
        if not device_data:
            raise KeyError(f"Missing key: {self.TYPE_OF_DEVICE}")

        # Восстанавливаем вложенные объекты PowerSupplyChannel
        if 'channels' in device_data:
            channels = []
            for ch_data in device_data['channels']:
                channels.append(PowerSupplyChannel(**ch_data))
            device_data['channels'] = channels

        # Обновляем остальные поля
        for key, value in device_data.items():
            if hasattr(self.value, key):
                setattr(self.value, key, value)

    def test_channel_max(self, read_current: list[float]) -> list[bool | None]:
        more_then_max: list[bool | None] = []
        for ch, read_curr in zip(self.value.channels, read_current):
            if ch.is_readable and read_curr is not None and ch.is_enabled:
                more_then_max.append(ch.max_rating is not None and ch.max_rating <= read_curr)
            else:
                more_then_max.append(None)
        return more_then_max

    def test_channel_typ(self, read_current: list[float]) -> list[bool | None]:
        more_than_typ: list[bool | None] = []
        for ch, read_curr in zip(self.value.channels, read_current):
            if ch.is_readable and read_curr is not None and ch.is_enabled:
                more_than_typ.append(ch.typical_rating is not None and ch.typical_rating <= read_curr)
            else:
                more_than_typ.append(None)
        return more_than_typ

    def clear(self) -> None:
        for ch in self.value.channels:
            ch.max_rating = None
            ch.typical_rating = None

    def create_conditions(self) -> str:
        return ', '.join(
            f'V{ch.name} = {ch.volt} В'
            for ch in self.value.channels
            if ch.name
        )

    def create_datasheet(self) -> str:
        specs = []
        for ch in filter(lambda c: c.is_readable, self.value.channels):
            if ch.max_rating is not None:
                specs.append(f'ток I{ch.name} должен быть меньше {ch.max_rating * 1000} мА')
            if ch.typical_rating is not None:
                specs.append(f'типовое значение I{ch.name} = {ch.typical_rating * 1000} мА')
        return ', '.join(specs)


if __name__ == "__main__":
    # Создание и заполнение объекта
    ps = PowerSupplyDO()
    ps.value.channels[0].name = "VCC"
    ps.value.channels[0].max_rating = 0.5
    ps.value.channels[1].name = "GND"

    # Выгрузка в словарь
    ps_dict = ps.to_dict()
    print("Словарь PowerSupply:", ps_dict)

    # Загрузка из словаря
    new_ps = PowerSupplyDO()
    new_ps.update_from_dict(ps_dict)

    # Проверка, что channels - это объекты PowerSupplyChannel
    print("\nТипы channels после загрузки:")
    for ch in new_ps.value.channels:
        print(type(ch), ch)

    # Генерация и вывод данных
    conditions = new_ps.create_conditions()
    datasheet = new_ps.create_datasheet()

    print("\nРезультаты после загрузки:")
    print("Условия:", conditions)
    print("Даташит:", datasheet)

    # Тестирование проверки токов
    test_currents = [0.3, 0.1, None]
    print("Проверка max:", new_ps.test_channel_max(test_currents))
    print("Проверка typ:", new_ps.test_channel_typ(test_currents))