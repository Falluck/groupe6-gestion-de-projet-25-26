import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock RPi.GPIO avant l'import
mock_gpio_module = MagicMock()
mock_gpio_module.BCM = 11
mock_gpio_module.OUT = 0
mock_gpio_module.IN = 1
mock_gpio_module.HIGH = 1
mock_gpio_module.LOW = 0
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = mock_gpio_module

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

import DistanceSensor as ds_module
from DistanceSensor import DistanceSensor


class TestDistanceSensor(unittest.TestCase):
    """Tests pour la classe DistanceSensor (code vide)."""

    def setUp(self):
        self.mock_gpio = MagicMock()
        self.mock_gpio.BCM = 11
        self.mock_gpio.OUT = 0
        self.mock_gpio.IN = 1
        self.mock_gpio.HIGH = 1
        self.mock_gpio.LOW = 0

    def test_creation_side_capitalise(self):
        """Vérifie que le côté est capitalisé automatiquement."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(16, 25, "front")
        self.assertEqual(sensor.side, "Front")

    def test_creation_side_majuscule(self):
        """Vérifie la capitalisation depuis des majuscules."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(1, 2, "LEFT")
        self.assertEqual(sensor.side, "Left")

    def test_gpio_setup_appele_deux_fois(self):
        """Vérifie que GPIO.setup est appelé 2 fois (trig + echo)."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(16, 25, "front")
        self.assertEqual(self.mock_gpio.setup.call_count, 2)

    def test_read_value_existe_et_appelable(self):
        """Vérifie que readValue existe et peut être appelée."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(16, 25, "front")
            result = sensor.readValue()
        # Méthode en pass → retourne None
        self.assertIsNone(result)

    def test_heritage_sensor(self):
        """Vérifie que DistanceSensor hérite de Sensor."""
        from Sensor import Sensor
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(16, 25, "front")
        self.assertIsInstance(sensor, Sensor)

    def test_propriete_side_lecture_seule(self):
        """Vérifie que side est en lecture seule."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(16, 25, "front")
        with self.assertRaises(AttributeError):
            sensor.side = "Back"


if __name__ == '__main__':
    unittest.main(verbosity=2)
