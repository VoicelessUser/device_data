from device_dc import VNA
from data_operate import DataOperate

class VNADO(DataOperate):
    TYPE_OF_DEVICE = 'VNA'
    def __init__(self, vna: VNA= None):
        if vna is None:
            vna = VNA()
        super().__init__(vna)

    def create_conditions(self) -> str:
        """Формирует условия измерения VNA"""
        freqs = ', '.join(f'{f / 1e9:.3f} ГГц' for f in self.value.targ_freq.keys())
        return f'входная мощность = {self.value.power} дБм, частоты: {freqs}'

    def create_datasheet(self) -> str:
        """Формирует спецификацию по S21"""
        specs = []
        for freq, lim in self.value.targ_freq.items():
            freq_ghz = f'{freq / 1e9:.3f} ГГц'
            min_val = lim.get('min')
            max_val = lim.get('max')
            typ_val = lim.get('typ')
            if min_val is not None and max_val is not None:
                specs.append(f'S21 на частоте {freq_ghz} должен находится в диапазоне {min_val}..{max_val} дБ')
            elif min_val is not None:
                specs.append(f'S21 на частоте {freq_ghz} должен быть не менее {min_val} дБ')
            elif max_val is not None:
                specs.append(f'S21 на частоте {freq_ghz} должен быть не более {max_val} дБ')
            elif typ_val is not None:
                specs.append(f'S21 на частоте {freq_ghz} должен быть ≈ {typ_val} дБ')
        return ', '.join(specs)

if __name__ == "__main__":
    # Создание и заполнение объекта
    vna = VNADO()
    vna.value.power = 10.0
    vna.value.targ_freq = {
        1e9: {'min': -20, 'max': -10},
        2e9: {'typ': -15}
    }

    # Выгрузка в словарь
    vna_dict = vna.to_dict()
    print("\nСловарь VNA:", vna_dict)

    # Загрузка из словаря
    new_vna = VNADO()
    new_vna.update_from_dict(vna_dict)

    # Генерация и вывод данных
    conditions = new_vna.create_conditions()
    datasheet = new_vna.create_datasheet()

    print("\nРезультаты после загрузки:")
    print("Условия:", conditions)
    print("Даташит:", datasheet)


