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

from data.DistanceData import DistanceData
from data.RGBData import RGBData


class TestCar(unittest.TestCase):
    """Tests pour la classe Car."""

    def setUp(self):
        from Car import Car
        self.Car = Car
        self.mock_i2c = MagicMock()
        self.car = self.Car(self.mock_i2c)

        self.mock_motor = MagicMock()
        self.mock_sensor = MagicMock()
        self.car._Car__motorManager = self.mock_motor
        self.car._Car__sensorManager = self.mock_sensor

    @patch('Car.time')
    def test_prepare_motors_teste_avant_arriere_et_servo(self, mock_time):
        """Vérifie que prepareMotors teste les DC (avant/arrière) et le servo."""
        self.car.prepareMotors()
        vitesses = [c[0][0] for c in self.mock_motor.setSpeed.call_args_list]
        self.assertTrue(any(v > 0 for v in vitesses))
        self.assertTrue(any(v < 0 for v in vitesses))
        self.assertIn(0, vitesses)
        self.assertTrue(self.mock_motor.setAngle.called)

    def test_prepare_sensors_tous_ok(self):
        """Vérifie que prepareSensors retourne True quand tout fonctionne."""
        mock_rgb = MagicMock()
        mock_rgb.readValue.return_value = RGBData(100, 200, 50)
        self.mock_sensor._SensorManager__rgbSensor = mock_rgb
        self.mock_sensor.getCurrent.return_value = 250.0
        self.mock_sensor.getDistance.return_value = DistanceData(30.0, 20.0, 25.0)
        self.mock_sensor.detectLine.return_value = False
        self.assertTrue(self.car.prepareSensors())

    def test_prepare_sensors_retourne_false_si_rgb_echoue(self):
        """Vérifie que prepareSensors retourne False si le capteur RGB échoue."""
        mock_rgb = MagicMock()
        mock_rgb.readValue.side_effect = Exception("Déconnecté")
        self.mock_sensor._SensorManager__rgbSensor = mock_rgb
        self.mock_sensor.getCurrent.return_value = 250.0
        self.mock_sensor.getDistance.return_value = DistanceData(30.0, 20.0, 25.0)
        self.mock_sensor.detectLine.return_value = False
        self.assertFalse(self.car.prepareSensors())

    def test_prepare_sensors_retourne_false_si_ina_echoue(self):
        """Vérifie que prepareSensors retourne False si INA219 retourne None."""
        mock_rgb = MagicMock()
        mock_rgb.readValue.return_value = RGBData(100, 200, 50)
        self.mock_sensor._SensorManager__rgbSensor = mock_rgb
        self.mock_sensor.getCurrent.return_value = None
        self.mock_sensor.getDistance.return_value = DistanceData(30.0, 20.0, 25.0)
        self.mock_sensor.detectLine.return_value = False
        self.assertFalse(self.car.prepareSensors())

    def test_prepare_sensors_retourne_false_si_distance_echoue(self):
        """Vérifie que prepareSensors retourne False si getDistance retourne None."""
        mock_rgb = MagicMock()
        mock_rgb.readValue.return_value = RGBData(100, 200, 50)
        self.mock_sensor._SensorManager__rgbSensor = mock_rgb
        self.mock_sensor.getCurrent.return_value = 250.0
        self.mock_sensor.getDistance.return_value = None
        self.mock_sensor.detectLine.return_value = False
        self.assertFalse(self.car.prepareSensors())

    def test_prepare_sensors_retourne_false_si_ligne_echoue(self):
        """Vérifie que prepareSensors retourne False si detectLine lève une exception."""
        mock_rgb = MagicMock()
        mock_rgb.readValue.return_value = RGBData(100, 200, 50)
        self.mock_sensor._SensorManager__rgbSensor = mock_rgb
        self.mock_sensor.getCurrent.return_value = 250.0
        self.mock_sensor.getDistance.return_value = DistanceData(30.0, 20.0, 25.0)
        self.mock_sensor.detectLine.side_effect = Exception("Erreur ligne")
        self.assertFalse(self.car.prepareSensors())

    def test_logger_initialise(self):
        """Vérifie que le logger est initialisé."""
        import logging
        self.assertIsInstance(self.car.logger, logging.Logger)

    @patch('Car.time')
    def test_uturn_ecrit_dans_les_logs(self, mock_time):
        """Vérifie que uTurn produit des entrées dans les logs."""
        with patch.object(self.car.logger, 'info') as mock_log:
            self.car.uTurn()
            msgs = [c[0][0] for c in mock_log.call_args_list]
            self.assertTrue(any("demi-tour" in m.lower() for m in msgs))

    @patch('Car.time')
    def test_uturn_termine_vitesse_a_zero(self, mock_time):
        """Vérifie que uTurn remet la vitesse à 0 à la fin."""
        self.car.uTurn()
        last = self.mock_motor.setSpeed.call_args_list[-1]
        self.assertEqual(last[0][0], 0)

    def test_stop_car_met_vitesse_et_angle_a_zero(self):
        """Vérifie que stopCar met vitesse et angle à 0."""
        self.car.stopCar()
        self.mock_motor.setSpeed.assert_called_with(0)
        self.mock_motor.setAngle.assert_called_with(0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
