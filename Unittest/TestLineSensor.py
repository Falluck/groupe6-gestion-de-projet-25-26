import unittest
from unittest.mock import MagicMock, patch
import sys
import os

mock_gpio_module = MagicMock()
mock_gpio_module.BCM = 11
mock_gpio_module.OUT = 0
mock_gpio_module.IN = 1
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = mock_gpio_module

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

import LineSensor as ls_module
from LineSensor import LineSensor


class TestLineSensor(unittest.TestCase):
    """Tests pour la classe LineSensor."""

    def setUp(self):
        self.mock_gpio = MagicMock()
        self.mock_gpio.BCM = 11
        self.mock_gpio.IN = 1

    def test_creation_attribut(self):
        """Vérifie que le pin GPIO est correctement stocké."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
        self.assertEqual(sensor.pinGPIO, 20)

    def test_gpio_setup_appele_sans_setmode(self):
        """Vérifie que GPIO.setup est appelé mais pas setmode."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
        self.mock_gpio.setup.assert_called_with(20, self.mock_gpio.IN)
        self.mock_gpio.setmode.assert_not_called()

    def test_read_value_ligne_detectee(self):
        """Vérifie que readValue retourne True quand GPIO = 0."""
        self.mock_gpio.input.return_value = 0
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
            result = sensor.readValue()
        self.assertTrue(result)

    def test_read_value_pas_de_ligne(self):
        """Vérifie que readValue retourne False quand GPIO = 1."""
        self.mock_gpio.input.return_value = 1
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
            result = sensor.readValue()
        self.assertFalse(result)

    def test_propriete_lecture_seule(self):
        """Vérifie que pinGPIO est en lecture seule."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
        with self.assertRaises(AttributeError):
            sensor.pinGPIO = 99

    def test_creation_pin_negatif(self):
        """Vérifie que pinGPIO négatif lève ValueError."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                LineSensor(-1)

    def test_creation_pin_string(self):
        """Vérifie que pinGPIO string lève ValueError."""
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                LineSensor("abc")

    def test_read_value_timeout(self):
        """Vérifie que readValue lève TimeoutError si GPIO ne donne ni 0 ni 1."""
        self.mock_gpio.input.return_value = -1

        mock_time = MagicMock()
        mock_time.time.side_effect = [0.0, 0.0, 2.0]
        mock_time.sleep = MagicMock()

        with patch.object(ls_module, 'GPIO', self.mock_gpio), \
             patch.object(ls_module, 'time', mock_time):
            sensor = LineSensor(20)
            with self.assertRaises(TimeoutError):
                sensor.readValue()

    def test_gpio_input_leve_exception(self):
        """Vérifie le comportement si GPIO.input lève une exception."""
        self.mock_gpio.input.side_effect = RuntimeError("GPIO erreur")
        with patch.object(ls_module, 'GPIO', self.mock_gpio):
            sensor = LineSensor(20)
            with self.assertRaises(RuntimeError):
                sensor.readValue()


if __name__ == '__main__':
    unittest.main(verbosity=2)
