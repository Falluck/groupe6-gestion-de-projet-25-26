import unittest
from unittest.mock import MagicMock
import sys
import os

mock_gpio = MagicMock()
mock_gpio.BCM = 11
mock_gpio.OUT = 0
mock_gpio.IN = 1
mock_gpio.HIGH = 1
mock_gpio.LOW = 0
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = mock_gpio
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()

mock_pca = MagicMock()
sys.modules['adafruit_pca9685'] = mock_pca

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from MotorManager import MotorManager
from ServoMotor import ServoMotor


class TestMotorManager(unittest.TestCase):
    """Tests pour la classe MotorManager (code vide)."""

    def setUp(self):
        mock_gpio.reset_mock()
        mock_pca.reset_mock()
        self.mock_pwm = MagicMock()
        mock_pca.PCA9685.return_value = self.mock_pwm
        self.mock_i2c = MagicMock()
        self.manager = MotorManager(self.mock_i2c)

    def test_creation_pca9685(self):
        """Vérifie que le driver PCA9685 est initialisé avec la bonne adresse."""
        mock_pca.PCA9685.assert_called_with(self.mock_i2c, address=0x40)

    def test_creation_frequence(self):
        """Vérifie que la fréquence PWM est réglée à 50 Hz."""
        self.assertEqual(self.mock_pwm.frequency, 50)

    def test_set_speed_existe_et_appelable(self):
        """Vérifie que setSpeed existe et peut être appelée."""
        result = self.manager.setSpeed(50)
        self.assertIsNone(result)

    def test_set_speed_zero_appelable(self):
        """Vérifie que setSpeed(0) ne crashe pas."""
        result = self.manager.setSpeed(0)
        self.assertIsNone(result)

    def test_set_speed_negatif_appelable(self):
        """Vérifie que setSpeed(-50) ne crashe pas."""
        result = self.manager.setSpeed(-50)
        self.assertIsNone(result)

    def test_set_angle_existe_et_appelable(self):
        """Vérifie que setAngle existe et peut être appelée."""
        result = self.manager.setAngle(0)
        self.assertIsNone(result)

    def test_convert_steering_to_duty_existe_et_appelable(self):
        """Vérifie que convert_steering_to_duty existe et peut être appelée."""
        result = self.manager.convert_steering_to_duty(0)
        self.assertIsNone(result)

    def test_servo_properties_duty(self):
        """Vérifie que minDuty et maxDuty du servo sont accessibles."""
        servo = self.manager._MotorManager__servoDirection
        self.assertEqual(servo.minDuty, 6.0)
        self.assertEqual(servo.maxDuty, 10.0)

    def test_deux_moteurs_dc_crees(self):
        """Vérifie que 2 moteurs DC sont créés."""
        motors = self.manager._MotorManager__dcMotorsPropulsion
        self.assertEqual(len(motors), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
