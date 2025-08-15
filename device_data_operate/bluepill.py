from dataclasses import asdict

from device_dc import BluePill

class BluePillDO:

    def __init__(self):
        self.data = BluePill()
        super().__init__()

    def create_spi_message_list(self) -> list[int]:
        """Создание списка команд для SPI интерфейса"""
        message_list = [0] + [2 ** i for i in range(self.data.num_of_bits)] + [255]

        if self.data.inversion:
            message_list = [255 - message for message in message_list]

        return message_list

    def create_list_par_messages(self) -> list[set]:
        """Создание списка поднятых пинов для PAR интерфейса"""
        message_list = [set()] + [{i + 1} for i in range(self.data.num_of_bits)] + [self.data.ALL_PINS]

        if self.data.inversion:
            message_list = [self.data.ALL_PINS - message for message in message_list]

        return message_list

    def create_message_heading(self, message: int|set) -> str:
        if isinstance(message, int) and self.data.type_inter_spi:
            heading = f'SPI [{message:b}]:'
        elif isinstance(message, set) and not self.data.type_inter_spi:
            heading = f'pin High [{message if message != set() else ""}], pin Low [{self.data.ALL_PINS - message if message != self.data.ALL_PINS else ""}]'
        else:
            heading = 'Неверный формат данных'
        return heading

    def shift_to_dict(self) -> dict[str, dict]:
        return {
            'bluepill': asdict(self.data)
        }

    def from_dict_to_data(self, data_dict: dict[str, dict]) -> None:
        """Обновляет данные из словаря, используя автоматическое преобразование."""
        bluepill_data = data_dict.get('bluepill')
        if not bluepill_data:
            return

        # Обновляем поля data (без замены самого объекта)
        for key, value in bluepill_data.items():
            if hasattr(self.data, key):
                setattr(self.data, key, value)

