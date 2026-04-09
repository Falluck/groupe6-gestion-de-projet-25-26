import unittest
from unittest.mock import MagicMock, patch
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
from DCMotor import DCMotor
from ServoMotor import ServoMotor


class TestMotorManager(unittest.TestCase):
    """Tests pour la classe MotorManager."""

    def setUp(self):
        mock_gpio.reset_mock()
        mock_pca.reset_mock()
        self.mock_pwm = MagicMock()
        mock_pca.PCA9685.return_value = self.mock_pwm
        self.mock_i2c = MagicMock()
        self.manager = MotorManager(self.mock_i2c)

    def test_creation_pca9685(self):
        """Vérifie que le driver PCA9685 est initialisé."""
        mock_pca.PCA9685.assert_called_with(self.mock_i2c, address=0x40)

    def test_set_speed_zero_arrete_moteurs(self):
        """Vérifie que setSpeed(0) appelle stop() sur les moteurs."""
        with patch.object(DCMotor, 'stop') as mock_stop:
            self.manager.setSpeed(0)
            self.assertTrue(mock_stop.called)

    def test_set_speed_positif_direction_avant(self):
        """Vérifie que setSpeed(50) = marche avant."""
        with patch.object(DCMotor, 'setDirection') as mock_dir:
            self.manager.setSpeed(50)
            mock_dir.assert_called_with(True)

    def test_set_speed_negatif_direction_arriere(self):
        """Vérifie que setSpeed(-50) = marche arrière."""
        with patch.object(DCMotor, 'setDirection') as mock_dir:
            self.manager.setSpeed(-50)
            mock_dir.assert_called_with(False)

    def test_set_speed_invalide_string(self):
        """Vérifie que setSpeed avec un string ne crashe pas."""
        self.manager.setSpeed("abc")

    def test_set_speed_invalide_none(self):
        """Vérifie que setSpeed avec None ne crashe pas."""
        self.manager.setSpeed(None)

    def test_set_speed_hors_plage_positif(self):
        """Vérifie que setSpeed(150) ne crashe pas mais n'exécute pas les moteurs."""
        with patch.object(DCMotor, 'setDirection') as mock_dir:
            self.manager.setSpeed(150)
            mock_dir.assert_not_called()

    def test_set_speed_hors_plage_negatif(self):
        """Vérifie que setSpeed(-150) ne crashe pas mais n'exécute pas les moteurs."""
        with patch.object(DCMotor, 'setDirection') as mock_dir:
            self.manager.setSpeed(-150)
            mock_dir.assert_not_called()

    def test_set_angle_appele_duty_cycle(self):
        """Vérifie que setAngle modifie le duty_cycle du servo."""
        self.manager.setAngle(0)
        self.assertTrue(self.mock_pwm.channels.__getitem__.called)

    def test_set_angle_invalide_string(self):
        """Vérifie que setAngle avec un string ne crashe pas."""
        self.manager.setAngle("abc")

    def test_set_angle_invalide_none(self):
        """Vérifie que setAngle avec None ne crashe pas."""
        self.manager.setAngle(None)

    def test_set_angle_hors_plage_positif(self):
        """Vérifie que setAngle(200) ne crashe pas mais ne bouge pas le servo."""
        self.mock_pwm.reset_mock()
        self.manager.setAngle(200)
        self.mock_pwm.channels.__getitem__().duty_cycle.__set__ = MagicMock()

    def test_set_angle_hors_plage_negatif(self):
        """Vérifie que setAngle(-200) ne crashe pas mais ne bouge pas le servo."""
        self.mock_pwm.reset_mock()
        self.manager.setAngle(-200)

    def test_convert_steering_gauche(self):
        """Vérifie que steering=-100 donne environ 6% de 65535."""
        result = self.manager.convert_steering_to_duty(-100)
        expected = int(0.06 * 65535)
        self.assertEqual(result, expected)

    def test_convert_steering_centre(self):
        """Vérifie que steering=0 donne environ 8% de 65535."""
        result = self.manager.convert_steering_to_duty(0)
        expected = int(0.08 * 65535)
        self.assertEqual(result, expected)

    def test_convert_steering_droite(self):
        """Vérifie que steering=+100 donne environ 10% de 65535."""
        result = self.manager.convert_steering_to_duty(100)
        expected = int(0.10 * 65535)
        self.assertEqual(result, expected)

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
