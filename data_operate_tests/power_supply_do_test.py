import unittest
from dataclasses import asdict
from device_data_operate import PowerSupplyDO


class TestPowerSupplyDO(unittest.TestCase):
    def setUp(self):
        self.ps = PowerSupplyDO()

    def test_shift_to_dict_and_back(self):
        """Тест преобразования в словарь и обратно"""
        # Сохраняем исходное состояние
        original_data = self.ps.shift_to_dict()

        # Модифицируем данные
        modified_dict = {
            'power_supply': {
                'channels': [
                    {'number': 1, 'volt': 3.3, 'name': 'VCC', 'is_enabled': False},
                    {'number': 2, 'max_current': 0.5},
                    # Канал 3 не трогаем
                ]
            }
        }

        # Загружаем модифицированные данные
        self.ps.from_dict_to_data(modified_dict)

        # Проверяем изменения
        self.assertEqual(self.ps.data.channels[0].volt, 3.3)
        self.assertEqual(self.ps.data.channels[0].name, 'VCC')
        self.assertFalse(self.ps.data.channels[0].is_enabled)
        self.assertEqual(self.ps.data.channels[1].max_current, 0.5)

        # Проверяем, что канал 3 остался без изменений (по умолчанию is_enabled=False)
        self.assertFalse(self.ps.data.channels[2].is_enabled)

        # Возвращаем исходные данные
        self.ps.from_dict_to_data(original_data)
        self.assertEqual(self.ps.shift_to_dict(), original_data)

    def test_test_channel_max(self):
        """Тест проверки превышения максимального тока"""
        # Устанавливаем максимальные значения
        self.ps.data.channels[0].max_rating = 1.0
        self.ps.data.channels[1].max_rating = 0.5

        # Канал 2 не readable (is_readable=False), канал 3 disabled (is_enabled=False)
        test_currents = [1.1, 0.4]  # Только для первых двух каналов
        results = self.ps.test_channel_max(test_currents)

        # Ожидаем [True (превышен), None (канал 2 не readable)]
        self.assertEqual(results, [True, None])

    def test_test_channel_typ(self):
        """Тест проверки превышения типового тока"""
        self.ps.data.channels[0].typical_rating = 0.8
        self.ps.data.channels[1].typical_rating = 0.3

        test_currents = [0.9, 0.2]  # Только для первых двух каналов
        results = self.ps.test_channel_typ(test_currents)

        # Ожидаем [True (превышен), None (канал 2 не readable)]
        self.assertEqual(results, [True, None])

    def test_clear(self):
        """Тест очистки рейтингов"""
        # Устанавливаем значения
        for ch in self.ps.data.channels:
            ch.max_rating = 1.0
            ch.typical_rating = 0.5

        self.ps.clear()

        for ch in self.ps.data.channels:
            self.assertIsNone(ch.max_rating)
            self.assertIsNone(ch.typical_rating)

    def test_create_conditions(self):
        """Тест формирования условий"""
        self.ps.data.channels[0].name = "CC"
        self.ps.data.channels[0].volt = 3.3
        self.ps.data.channels[1].name = ""  # Не должно попасть в вывод

        conditions = self.ps.create_conditions()
        self.assertEqual(conditions, "VCC = 3.3 В")

    def test_empty_dict_handling(self):
        """Тест обработки пустого словаря"""
        original_data = self.ps.shift_to_dict()
        self.ps.from_dict_to_data({})
        self.assertEqual(self.ps.shift_to_dict(), original_data)

    def test_partial_dict_handling(self):
        """Тест обработки частичного словаря"""
        self.ps.from_dict_to_data({
            'power_supply': {
                'channels': [
                    {'number': 1, 'volt': 12.0}
                ]
            }
        })
        self.assertEqual(self.ps.data.channels[0].volt, 12.0)
        # Проверяем, что другие поля не изменились
        self.assertEqual(self.ps.data.channels[0].name, '')
        self.assertTrue(self.ps.data.channels[0].is_enabled)


if __name__ == '__main__':
    unittest.main()
