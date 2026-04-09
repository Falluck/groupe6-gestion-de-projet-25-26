import unittest
from unittest.mock import MagicMock, patch
import sys
import os


sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['adafruit_tcs34725'] = MagicMock()
sys.modules['adafruit_ina219'] = MagicMock()
sys.modules['adafruit_pca9685'] = MagicMock()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))


class TestCar(unittest.TestCase):
    """Tests pour la classe Car (code vide)."""

    def setUp(self):
        from Car import Car
        self.Car = Car
        self.mock_i2c = MagicMock()
        self.car = self.Car(self.mock_i2c)

        self.mock_motor = MagicMock()
        self.mock_sensor = MagicMock()
        self.car._Car__motorManager = self.mock_motor
        self.car._Car__sensorManager = self.mock_sensor

    def test_creation_sans_erreur(self):
        """Vérifie que Car peut être instancié."""
        self.assertIsNotNone(self.car)

    def test_logger_initialise(self):
        """Vérifie que le logger est initialisé."""
        import logging
        self.assertIsInstance(self.car.logger, logging.Logger)

    def test_prepare_motors_existe_et_appelable(self):
        """Vérifie que prepareMotors existe et peut être appelée."""
        result = self.car.prepareMotors()

        self.assertIsNone(result)

    def test_prepare_sensors_existe_et_appelable(self):
        """Vérifie que prepareSensors existe et peut être appelée."""
        result = self.car.prepareSensors()
        self.assertIsNone(result)

    def test_start_car_existe_et_appelable(self):
        """Vérifie que startCar existe et peut être appelée."""
        result = self.car.startCar()
        self.assertIsNone(result)

    def test_stop_car_existe_et_appelable(self):
        """Vérifie que stopCar existe et peut être appelée."""
        result = self.car.stopCar()
        self.assertIsNone(result)

    def test_u_turn_existe_et_appelable(self):
        """Vérifie que uTurn existe et peut être appelée."""
        result = self.car.uTurn()
        self.assertIsNone(result)

    def test_attributs_internes(self):
        """Vérifie que les attributs internes sont initialisés."""
        car = self.Car(self.mock_i2c)
        self.assertEqual(car._Car__carName, "Car")
        self.assertEqual(car._Car__tour, -1)
        self.assertEqual(car._Car__totalLaps, 0)
        self.assertFalse(car._Car__last_line_state)

    def test_motor_manager_existe(self):
        """Vérifie que le MotorManager interne est créé."""
        car = self.Car(self.mock_i2c)
        self.assertIsNotNone(car._Car__motorManager)

    def test_sensor_manager_existe(self):
        """Vérifie que le SensorManager interne est créé."""
        car = self.Car(self.mock_i2c)
        self.assertIsNotNone(car._Car__sensorManager)


if __name__ == '__main__':
    unittest.main(verbosity=2)
