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

    def test_gpio_setup_appele_deux_fois(self):
        """Vérifie que GPIO.setup est appelé 2 fois (input1, input2) mais pas pour enable."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
        self.assertEqual(self.mock_gpio.setup.call_count, 2)

    def test_gpio_setmode_pas_appele(self):
        """Vérifie que GPIO.setmode n'est PAS appelé (centralisé dans main)."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
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

    def test_creation_pins_negatifs(self):
        """Vérifie que le constructeur accepte des pins négatifs (pas de validation)."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(-1, -2, -3)
        self.assertEqual(motor.pinEnable, -1)
        self.assertEqual(motor.pinInput1, -2)
        self.assertEqual(motor.pinInput2, -3)

    def test_creation_pins_zero(self):
        """Vérifie que le constructeur accepte des pins à zéro."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(0, 0, 0)
        self.assertEqual(motor.pinEnable, 0)

    def test_gpio_setup_echoue(self):
        """Vérifie le comportement si GPIO.setup lève une exception."""
        self.mock_gpio.setup.side_effect = RuntimeError("GPIO non initialisé")
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(RuntimeError):
                DCMotor(5, 17, 18)

    def test_gpio_output_echoue_sur_direction(self):
        """Vérifie le comportement si GPIO.output lève une exception."""
        self.mock_gpio.output.side_effect = RuntimeError("GPIO erreur")
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
            with self.assertRaises(RuntimeError):
                motor.setDirection(True)

    def test_gpio_output_echoue_sur_stop(self):
        """Vérifie le comportement si GPIO.output lève une exception sur stop."""
        self.mock_gpio.output.side_effect = RuntimeError("GPIO erreur")
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
            with self.assertRaises(RuntimeError):
                motor.stop()


if __name__ == '__main__':
    unittest.main(verbosity=2)
