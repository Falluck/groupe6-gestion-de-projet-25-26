import unittest
from unittest.mock import MagicMock, patch
import sys
import os

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
    """Tests pour la classe DCMotor (code vide)."""

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

    def test_gpio_setup_appele_trois_fois(self):
        """Vérifie que GPIO.setup est appelé 3 fois (enable, input1, input2)."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
        self.assertEqual(self.mock_gpio.setup.call_count, 3)

    def test_gpio_setmode_pas_appele(self):
        """Vérifie que GPIO.setmode n'est PAS appelé (centralisé dans main)."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
        self.mock_gpio.setmode.assert_not_called()

    def test_set_direction_existe_et_appelable(self):
        """Vérifie que setDirection existe et peut être appelée sans erreur."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
            result = motor.setDirection(True)
        self.assertIsNone(result)

    def test_stop_existe_et_appelable(self):
        """Vérifie que stop existe et peut être appelée sans erreur."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
            result = motor.stop()
        self.assertIsNone(result)

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
