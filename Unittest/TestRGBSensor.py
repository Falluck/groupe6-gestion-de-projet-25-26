import unittest
from unittest.mock import MagicMock
import sys
import os

sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['adafruit_tcs34725'] = MagicMock()
import adafruit_tcs34725
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from data.RGBData import RGBData
from RGBSensor import RGBSensor

class TestRGBSensor(unittest.TestCase):
    """Tests pour la classe RGBSensor."""

    def setUp(self):
        self.mock_tcs = MagicMock()
        adafruit_tcs34725.TCS34725.return_value = self.mock_tcs

        self.RGBSensor = RGBSensor

        self.mock_i2c = MagicMock()
        self.sensor = self.RGBSensor(self.mock_i2c)

    def test_read_value_retourne_rgb_data(self):
        """Vérifie que readValue retourne un objet RGBData."""
        self.mock_tcs.color_rgb_bytes = (120, 200, 50)
        result = self.sensor.readValue()
        self.assertIsInstance(result, RGBData)
        self.assertEqual(result.red, 120)
        self.assertEqual(result.green, 200)
        self.assertEqual(result.blue, 50)

    def test_read_value_noir(self):
        """Vérifie la lecture du noir (0, 0, 0)."""
        self.mock_tcs.color_rgb_bytes = (0, 0, 0)
        result = self.sensor.readValue()
        self.assertEqual(result.red, 0)

    def test_read_value_blanc(self):
        """Vérifie la lecture du blanc (255, 255, 255)."""
        self.mock_tcs.color_rgb_bytes = (255, 255, 255)
        result = self.sensor.readValue()
        self.assertEqual(result.red, 255)

    def test_heritage_i2c_sensor(self):
        """Vérifie que RGBSensor hérite de I2CSensor."""
        from I2CSensor import I2CSensor
        self.assertIsInstance(self.sensor, I2CSensor)

    def test_heritage_sensor(self):
        """Vérifie que RGBSensor hérite de Sensor (via I2CSensor)."""
        from Sensor import Sensor
        self.assertIsInstance(self.sensor, Sensor)

    def test_read_value_capteur_deconnecte(self):
        """Vérifie que readValue propage l'exception si le capteur est déconnecté."""
        type(self.mock_tcs).color_rgb_bytes = property(
            fget=MagicMock(side_effect=OSError("Capteur déconnecté"))
        )
        with self.assertRaises(OSError):
            self.sensor.readValue()


if __name__ == '__main__':
    unittest.main(verbosity=2)
