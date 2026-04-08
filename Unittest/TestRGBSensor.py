import unittest
from unittest.mock import MagicMock
import sys
import os

# Mock toutes les dépendances hardware
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['adafruit_tcs34725'] = MagicMock()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))


class TestRGBSensor(unittest.TestCase):
    """Tests pour la classe RGBSensor (code vide)."""

    def setUp(self):
        import adafruit_tcs34725
        self.mock_tcs = MagicMock()
        adafruit_tcs34725.TCS34725.return_value = self.mock_tcs

        from RGBSensor import RGBSensor
        self.RGBSensor = RGBSensor

        self.mock_i2c = MagicMock()
        self.sensor = self.RGBSensor(self.mock_i2c)

    def test_creation_sans_erreur(self):
        """Vérifie que le capteur peut être instancié avec un mock I2C."""
        self.assertIsNotNone(self.sensor)

    def test_read_value_existe_et_appelable(self):
        """Vérifie que readValue existe et peut être appelée."""
        result = self.sensor.readValue()
        # Méthode en pass → retourne None
        self.assertIsNone(result)

    def test_heritage_i2c_sensor(self):
        """Vérifie que RGBSensor hérite de I2CSensor."""
        from I2CSensor import I2CSensor
        self.assertIsInstance(self.sensor, I2CSensor)

    def test_heritage_sensor(self):
        """Vérifie que RGBSensor hérite de Sensor (via I2CSensor)."""
        from Sensor import Sensor
        self.assertIsInstance(self.sensor, Sensor)

    def test_i2c_bus_stocke(self):
        """Vérifie que le bus I2C est stocké dans l'attribut protégé."""
        self.assertEqual(self.sensor._i2c_bus, self.mock_i2c)


if __name__ == '__main__':
    unittest.main()
