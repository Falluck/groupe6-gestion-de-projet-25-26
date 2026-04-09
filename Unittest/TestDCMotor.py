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
        """Vérifie que GPIO.setup est appelé 2 fois (input1, input2)."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
        self.assertEqual(self.mock_gpio.setup.call_count, 2)

    def test_gpio_setmode_pas_appele(self):
        """Vérifie que GPIO.setmode n'est PAS appelé."""
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

    def test_creation_enable_negatif(self):
        """Vérifie que enable négatif lève ValueError."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                DCMotor(-1, 17, 18)

    def test_creation_input1_negatif(self):
        """Vérifie que input1 négatif lève ValueError."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                DCMotor(5, -1, 18)

    def test_creation_input2_negatif(self):
        """Vérifie que input2 négatif lève ValueError."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                DCMotor(5, 17, -1)

    def test_creation_enable_string(self):
        """Vérifie que enable string lève ValueError."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                DCMotor("abc", 17, 18)

    def test_set_direction_string(self):
        """Vérifie que setDirection avec un string lève TypeError."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
            with self.assertRaises(TypeError):
                motor.setDirection("avant")

    def test_set_direction_entier(self):
        """Vérifie que setDirection avec un entier lève TypeError."""
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            motor = DCMotor(5, 17, 18)
            with self.assertRaises(TypeError):
                motor.setDirection(1)

    def test_gpio_setup_echoue(self):
        """Vérifie le comportement si GPIO.setup lève une exception."""
        self.mock_gpio.setup.side_effect = RuntimeError("GPIO non initialisé")
        with patch.object(dc_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(RuntimeError):
                DCMotor(5, 17, 18)


if __name__ == '__main__':
    unittest.main(verbosity=2)
