import unittest
from unittest.mock import MagicMock
import sys
import os


sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['adafruit_ina219'] = MagicMock()
import adafruit_ina219

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from INASensor import INASensor
from I2CSensor import I2CSensor
from Sensor import Sensor

class TestINASensor(unittest.TestCase):
    """Tests pour la classe INASensor."""

    def setUp(self):
        self.mock_ina = MagicMock()
        adafruit_ina219.INA219.return_value = self.mock_ina

        self.INASensor = INASensor

        self.mock_i2c = MagicMock()
        self.sensor = self.INASensor(self.mock_i2c)

    def test_read_value_retourne_dict(self):
        """Vérifie que readValue retourne un dictionnaire avec les bonnes clés."""
        self.mock_ina.bus_voltage = 5.0
        self.mock_ina.shunt_voltage = 10.0
        self.mock_ina.current = 250.0

        result = self.sensor.readValue()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["BusVoltage"], 5.0)
        self.assertEqual(result["ShuntVoltage"], 0.01)
        self.assertEqual(result["Current"], 250.0)

    def test_read_value_valeurs_zero(self):
        """Vérifie la lecture avec des valeurs nulles."""
        self.mock_ina.bus_voltage = 0.0
        self.mock_ina.shunt_voltage = 0.0
        self.mock_ina.current = 0.0

        result = self.sensor.readValue()
        self.assertEqual(result["BusVoltage"], 0.0)
        self.assertEqual(result["Current"], 0.0)

    def test_heritage_i2c_sensor(self):
        """Vérifie que INASensor hérite de I2CSensor."""
        self.assertIsInstance(self.sensor, I2CSensor)

    def test_heritage_sensor(self):
        """Vérifie que INASensor hérite de Sensor (via I2CSensor)."""
        self.assertIsInstance(self.sensor, Sensor)

    def test_read_value_capteur_deconnecte(self):
        """Vérifie que readValue propage l'exception si le capteur est déconnecté."""
        type(self.mock_ina).bus_voltage = property(
            fget=MagicMock(side_effect=OSError("Capteur déconnecté"))
        )
        with self.assertRaises(OSError):
            self.sensor.readValue()


if __name__ == '__main__':
    unittest.main(verbosity=2)
