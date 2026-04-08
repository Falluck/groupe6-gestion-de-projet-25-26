import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock RPi.GPIO avant l'import
mock_gpio_module = MagicMock()
mock_gpio_module.BCM = 11
mock_gpio_module.OUT = 0
mock_gpio_module.IN = 1
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = mock_gpio_module

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

import LineSensor as ls_module
from LineSensor import LineSensor


class TestLineSensor(unittest.TestCase):
    """Tests pour la classe LineSensor (code vide)."""

    def setUp(self):
        self.mock_gpio = MagicMock()
        self.mock_gpio.BCM = 11
        self.mock_gpio.IN = 1

    def test_creation_attribut(self):
        """Vérifie que le pin GPIO est correctement stocké."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
        self.assertEqual(sensor.pinGPIO, 20)

    def test_gpio_setup_appele(self):
        """Vérifie que GPIO.setup est appelé avec le bon pin et IN."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
        self.mock_gpio.setup.assert_called_with(20, self.mock_gpio.IN)

    def test_gpio_setmode_pas_appele(self):
        """Vérifie que GPIO.setmode n'est PAS appelé."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
        self.mock_gpio.setmode.assert_not_called()

    def test_read_value_existe_et_appelable(self):
        """Vérifie que readValue existe et peut être appelée."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
            result = sensor.readValue()
        # Méthode en pass → retourne None
        self.assertIsNone(result)

    def test_heritage_sensor(self):
        """Vérifie que LineSensor hérite de Sensor."""
        from Sensor import Sensor
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
        self.assertIsInstance(sensor, Sensor)

    def test_propriete_lecture_seule(self):
        """Vérifie que pinGPIO est en lecture seule."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
        with self.assertRaises(AttributeError):
            sensor.pinGPIO = 99


if __name__ == '__main__':
    unittest.main(verbosity=2)
