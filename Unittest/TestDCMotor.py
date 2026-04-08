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

import DCMotor as dc_module
from DCMotor import DCMotor


class TestDCMotor(unittest.TestCase):
    """Tests pour la classe DCMotor."""

    def setUp(self):
        self.mock_gpio = MagicMock()
        self.mock_gpio.BCM = 11
        self.mock_gpio.OUT = 0
        self.mock_gpio.IN = 1
        self.mock_gpio.HIGH = 1
        self.mock_gpio.LOW = 0

    def test_creation_attributs(self):
        """Vérifie que les attributs sont correctement initialisés."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
        self.assertEqual(motor.pinEnable, 5)
        self.assertEqual(motor.pinInput1, 17)
        self.assertEqual(motor.pinInput2, 18)

    def test_gpio_setup_appele_sans_setmode(self):
        """Vérifie que GPIO.setup est appelé 3 fois mais pas setmode (centralisé dans main)."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
        self.assertEqual(self.mock_gpio.setup.call_count, 3)
        self.mock_gpio.setmode.assert_not_called()

    def test_set_direction_avant(self):
        """Vérifie la direction avant (True)."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
            motor.setDirection(True)
        self.mock_gpio.output.assert_any_call(17, 0)
        self.mock_gpio.output.assert_any_call(18, 1)

    def test_set_direction_arriere(self):
        """Vérifie la direction arrière (False)."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
            motor.setDirection(False)
        self.mock_gpio.output.assert_any_call(17, 1)
        self.mock_gpio.output.assert_any_call(18, 0)

    def test_stop(self):
        """Vérifie l'arrêt du moteur (freinage)."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
            motor.stop()
        self.mock_gpio.output.assert_any_call(17, 1)
        self.mock_gpio.output.assert_any_call(18, 1)

    def test_proprietes_lecture_seule(self):
        """Vérifie que les propriétés sont en lecture seule."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
        with self.assertRaises(AttributeError):
            motor.pinEnable = 99
        with self.assertRaises(AttributeError):
            motor.pinInput1 = 99
        with self.assertRaises(AttributeError):
            motor.pinInput2 = 99


if __name__ == '__main__':
    unittest.main(verbosity=2)
