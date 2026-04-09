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

import DistanceSensor as ds_module
from DistanceSensor import DistanceSensor


class TestDistanceSensor(unittest.TestCase):
    """Tests pour la classe DistanceSensor."""

    def setUp(self):
        self.mock_gpio = MagicMock()
        self.mock_gpio.BCM = 11
        self.mock_gpio.OUT = 0
        self.mock_gpio.IN = 1
        self.mock_gpio.HIGH = 1
        self.mock_gpio.LOW = 0

    def test_creation_attributs(self):
        """Vérifie la capitalisation du côté."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(16, 25, "front")
        self.assertEqual(sensor.side, "Front")

    def test_gpio_setup_appele(self):
        """Vérifie que les broches trigger et echo sont configurées."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(16, 25, "left")
        self.assertEqual(self.mock_gpio.setup.call_count, 2)

    def test_read_value_distance_valide(self):
        """Vérifie une mesure de distance valide (~17.15 cm)."""
        self.mock_gpio.input.side_effect = [0, 1, 1, 0]

        mock_time = MagicMock()
        mock_time.sleep = MagicMock()
        mock_time.time.side_effect = [1.0, 1.0, 1.0, 1.0, 1.001, 1.001]

        with patch.object(ds_module, 'GPIO', self.mock_gpio), \
             patch.object(ds_module, 'time', mock_time):
            sensor = DistanceSensor(16, 25, "front")
            result = sensor.readValue()

        self.assertIsNotNone(result)
        self.assertAlmostEqual(result, 17.15, places=1)

    def test_read_value_retourne_none_sur_erreur(self):
        """Vérifie que readValue retourne None en cas d'exception."""
        self.mock_gpio.input.side_effect = Exception("Erreur GPIO")
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(16, 25, "front")
            result = sensor.readValue()
        self.assertIsNone(result)

    def test_side_capitalise(self):
        """Vérifie que le côté est toujours capitalisé."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor1 = DistanceSensor(1, 2, "right")
            sensor2 = DistanceSensor(1, 2, "LEFT")
        self.assertEqual(sensor1.side, "Right")
        self.assertEqual(sensor2.side, "Left")

    def test_propriete_side_lecture_seule(self):
        """Vérifie que side est en lecture seule."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            sensor = DistanceSensor(16, 25, "front")
        with self.assertRaises(AttributeError):
            sensor.side = "Back"

    def test_creation_trig_negatif(self):
        """Vérifie que pinTrig négatif lève ValueError."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                DistanceSensor(-1, 25, "front")

    def test_creation_echo_negatif(self):
        """Vérifie que pinEcho négatif lève ValueError."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                DistanceSensor(16, -1, "front")

    def test_creation_side_vide(self):
        """Vérifie que side vide lève ValueError."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                DistanceSensor(16, 25, "")

    def test_creation_side_espaces(self):
        """Vérifie que side avec seulement des espaces lève ValueError."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                DistanceSensor(16, 25, "   ")

    def test_creation_side_entier(self):
        """Vérifie que side entier lève ValueError."""
        with patch.object(ds_module, 'GPIO', self.mock_gpio):
            with self.assertRaises(ValueError):
                DistanceSensor(16, 25, 123)

    def test_read_value_distance_trop_courte(self):
        """Vérifie que readValue retourne None si distance < 2 cm."""
        self.mock_gpio.input.side_effect = [0, 1, 1, 0]

        mock_time = MagicMock()
        mock_time.sleep = MagicMock()
        mock_time.time.side_effect = [1.0, 1.0, 1.0, 1.0, 1.00005, 1.00005]

        with patch.object(ds_module, 'GPIO', self.mock_gpio), \
             patch.object(ds_module, 'time', mock_time):
            sensor = DistanceSensor(16, 25, "front")
            result = sensor.readValue()
        self.assertIsNone(result)

    def test_read_value_distance_trop_longue(self):
        """Vérifie que readValue retourne None si distance > 400 cm."""
        self.mock_gpio.input.side_effect = [0, 1, 1, 0]

        mock_time = MagicMock()
        mock_time.sleep = MagicMock()
        mock_time.time.side_effect = [1.0, 1.0, 1.0, 1.0, 1.05, 1.05]

        with patch.object(ds_module, 'GPIO', self.mock_gpio), \
             patch.object(ds_module, 'time', mock_time):
            sensor = DistanceSensor(16, 25, "front")
            result = sensor.readValue()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
