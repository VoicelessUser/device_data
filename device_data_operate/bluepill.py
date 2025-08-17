from device_dc import BluePill
from data_operate import DataOperate

class BluePillDO(DataOperate):
    TYPE_OF_DEVICE = 'bluepill'

    def __init__(self, bluepill: BluePill = None):
        if bluepill is None:
            bluepill = BluePill()  # Создаём экземпляр по умолчанию
        super().__init__(bluepill)

    def create_spi_message_list(self) -> list[int]:
        """Создание списка команд для SPI интерфейса"""
        message_list = [0] + [2 ** i for i in range(self.value.num_of_bits)] + [255]

        if self.value.inversion:
            message_list = [255 - message for message in message_list]

        return message_list

    def create_list_par_messages(self) -> list[set]:
        """Создание списка поднятых пинов для PAR интерфейса"""
        message_list = [set()] + [{i + 1} for i in range(self.value.num_of_bits)] + [self.value.ALL_PINS]

        if self.value.inversion:
            message_list = [self.value.ALL_PINS - message for message in message_list]

        return message_list

    def create_message_heading(self, message: int|set) -> str:
        if isinstance(message, int) and self.value.type_inter_spi:
            heading = f'SPI [{message:b}]:'
        elif isinstance(message, set) and not self.value.type_inter_spi:
            heading = f'pin High [{message if message != set() else ""}], pin Low [{self.value.ALL_PINS - message if message != self.value.ALL_PINS else ""}]'
        else:
            heading = 'Неверный формат данных'
        return heading

if __name__ == "__main__":
    # Создание и заполнение объекта
    bp = BluePillDO()
    bp.value.num_of_bits = 8
    bp.value.inversion = False
    bp.value.type_inter_spi = True

    # Выгрузка в словарь
    bp_dict = bp.to_dict()
    print("Словарь BluePill:", bp_dict)

    # Загрузка из словаря (имитация)
    new_bp = BluePillDO()
    new_bp.update_from_dict(bp_dict)

    # Генерация и вывод данных
    spi_messages = new_bp.create_spi_message_list()
    par_messages = new_bp.create_list_par_messages()
    heading = new_bp.create_message_heading(42)  # Пример сообщения

    print("\nРезультаты после загрузки:")
    print("SPI сообщения:", spi_messages)
    print("PAR сообщения:", par_messages)
    print("Заголовок:", heading)
