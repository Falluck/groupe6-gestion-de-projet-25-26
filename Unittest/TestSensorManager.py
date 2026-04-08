import unittest
from unittest.mock import MagicMock
import sys
import os

# Mock toutes les dépendances hardware
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['adafruit_tcs34725'] = MagicMock()
sys.modules['adafruit_ina219'] = MagicMock()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from SensorManager import SensorManager


class TestSensorManager(unittest.TestCase):
    """Tests pour la classe SensorManager (code vide)."""

    def setUp(self):
        self.mock_i2c = MagicMock()
        self.manager = SensorManager(self.mock_i2c)

    def test_creation_sans_erreur(self):
        """Vérifie que le manager peut être instancié."""
        self.assertIsNotNone(self.manager)

    def test_detect_line_existe_et_appelable(self):
        """Vérifie que detectLine existe et peut être appelée."""
        result = self.manager.detectLine()
        # Méthode en pass → retourne None
        self.assertIsNone(result)

    def test_get_distance_existe_et_appelable(self):
        """Vérifie que getDistance existe et peut être appelée."""
        result = self.manager.getDistance()
        self.assertIsNone(result)

    def test_is_green_existe_et_appelable(self):
        """Vérifie que isGreen existe et peut être appelée."""
        result = self.manager.isGreen()
        self.assertIsNone(result)

    def test_is_green_avec_parametres(self):
        """Vérifie que isGreen accepte les paramètres personnalisés."""
        result = self.manager.isGreen(greenMinimum=50, deltaMinimum=10)
        self.assertIsNone(result)

    def test_is_red_existe_et_appelable(self):
        """Vérifie que isRed existe et peut être appelée."""
        result = self.manager.isRed()
        self.assertIsNone(result)

    def test_is_red_avec_parametres(self):
        """Vérifie que isRed accepte les paramètres personnalisés."""
        result = self.manager.isRed(redMinimum=200, deltaMinimum=50)
        self.assertIsNone(result)

    def test_get_current_existe_et_appelable(self):
        """Vérifie que getCurrent existe et peut être appelée."""
        result = self.manager.getCurrent()
        self.assertIsNone(result)

    def test_gpio_lock_existe(self):
        """Vérifie que le verrou GPIO est initialisé."""
        lock = self.manager._SensorManager__gpio_lock
        self.assertTrue(hasattr(lock, 'acquire'))
        self.assertTrue(hasattr(lock, 'release'))

    def test_capteurs_internes_existent(self):
        """Vérifie que tous les capteurs internes sont créés."""
        self.assertIsNotNone(self.manager._SensorManager__lineSensor)
        self.assertIsNotNone(self.manager._SensorManager__distSensorFront)
        self.assertIsNotNone(self.manager._SensorManager__distSensorLeft)
        self.assertIsNotNone(self.manager._SensorManager__distSensorRight)
        self.assertIsNotNone(self.manager._SensorManager__rgbSensor)
        self.assertIsNotNone(self.manager._SensorManager__inaSensor)


if __name__ == '__main__':
    unittest.main()
