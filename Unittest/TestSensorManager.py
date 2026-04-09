import unittest
from unittest.mock import MagicMock
import sys
import os

sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['busio'] = MagicMock()
sys.modules['board'] = MagicMock()
sys.modules['adafruit_tcs34725'] = MagicMock()
sys.modules['adafruit_ina219'] = MagicMock()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from data.DistanceData import DistanceData
from data.RGBData import RGBData


class TestSensorManager(unittest.TestCase):
    """Tests pour la classe SensorManager."""

    def _create_manager(self, line_val=False, dist_vals=(30.0, 20.0, 25.0),
                         rgb_vals=(100, 200, 50), current_val=250.0):
        """Helper : crée un SensorManager avec des capteurs mockés."""
        from SensorManager import SensorManager

        mock_i2c = MagicMock()
        manager = SensorManager(mock_i2c)

        mock_line = MagicMock()
        mock_line.readValue.return_value = line_val
        manager._SensorManager__lineSensor = mock_line

        for attr, val in [('__distSensorFront', dist_vals[0]),
                           ('__distSensorLeft', dist_vals[1]),
                           ('__distSensorRight', dist_vals[2])]:
            mock_dist = MagicMock()
            mock_dist.readValue.return_value = val
            setattr(manager, f'_SensorManager{attr}', mock_dist)

        mock_rgb = MagicMock()
        mock_rgb.readValue.return_value = RGBData(*rgb_vals)
        manager._SensorManager__rgbSensor = mock_rgb

        mock_ina = MagicMock()
        mock_ina.readValue.return_value = {"Current": current_val}
        manager._SensorManager__inaSensor = mock_ina

        return manager

    def test_detect_line_true(self):
        """Vérifie la détection de ligne quand le capteur IR lit True."""
        manager = self._create_manager(line_val=True)
        self.assertTrue(manager.detectLine())

    def test_detect_line_false(self):
        """Vérifie l'absence de ligne quand le capteur IR lit False."""
        manager = self._create_manager(line_val=False)
        self.assertFalse(manager.detectLine())

    def test_detect_line_exception(self):
        """Vérifie que detectLine retourne False en cas d'exception."""
        manager = self._create_manager()
        manager._SensorManager__lineSensor.readValue.side_effect = Exception("Erreur")
        self.assertFalse(manager.detectLine())

    def test_get_distance_retourne_distance_data(self):
        """Vérifie que getDistance retourne un DistanceData."""
        manager = self._create_manager(dist_vals=(30.0, 20.0, 25.0))
        result = manager.getDistance()
        self.assertIsInstance(result, DistanceData)
        self.assertAlmostEqual(result.front, 30.0, places=0)

    def test_get_distance_sequentiel(self):
        """Vérifie que getDistance lit chaque capteur 5 fois."""
        manager = self._create_manager(dist_vals=(10.0, 20.0, 30.0))
        manager.getDistance()
        self.assertEqual(manager._SensorManager__distSensorFront.readValue.call_count, 5)
        self.assertEqual(manager._SensorManager__distSensorLeft.readValue.call_count, 5)
        self.assertEqual(manager._SensorManager__distSensorRight.readValue.call_count, 5)

    def test_get_distance_capteur_en_erreur(self):
        """Vérifie que getDistance gère un capteur qui retourne None."""
        manager = self._create_manager()
        manager._SensorManager__distSensorFront.readValue.return_value = None
        result = manager.getDistance()
        self.assertIsNone(result.front)
        self.assertAlmostEqual(result.left, 20.0, places=0)

    def test_get_distance_tous_capteurs_en_erreur(self):
        """Vérifie que getDistance gère le cas où tous les capteurs retournent None."""
        manager = self._create_manager()
        manager._SensorManager__distSensorFront.readValue.return_value = None
        manager._SensorManager__distSensorLeft.readValue.return_value = None
        manager._SensorManager__distSensorRight.readValue.return_value = None
        result = manager.getDistance()
        self.assertIsNone(result.front)
        self.assertIsNone(result.left)
        self.assertIsNone(result.right)

    def test_is_green_vrai(self):
        """Vérifie la détection du vert."""
        manager = self._create_manager(rgb_vals=(100, 200, 50))
        self.assertTrue(manager.isGreen())

    def test_is_green_faux_rouge_dominant(self):
        """Vérifie que isGreen retourne False quand rouge domine."""
        manager = self._create_manager(rgb_vals=(200, 10, 10))
        self.assertFalse(manager.isGreen())

    def test_is_green_exception_capteur(self):
        """Vérifie que isGreen retourne False si le capteur lève une exception."""
        manager = self._create_manager()
        manager._SensorManager__rgbSensor.readValue.side_effect = Exception("Erreur")
        self.assertFalse(manager.isGreen())

    def test_is_red_vrai(self):
        """Vérifie la détection du rouge."""
        manager = self._create_manager(rgb_vals=(200, 50, 30))
        self.assertTrue(manager.isRed())

    def test_is_red_faux_vert_dominant(self):
        """Vérifie que isRed retourne False quand vert domine."""
        manager = self._create_manager(rgb_vals=(50, 200, 50))
        self.assertFalse(manager.isRed())

    def test_is_red_exception_capteur(self):
        """Vérifie que isRed retourne False si le capteur lève une exception."""
        manager = self._create_manager()
        manager._SensorManager__rgbSensor.readValue.side_effect = Exception("Erreur")
        self.assertFalse(manager.isRed())

    def test_get_current_valeur_normale(self):
        """Vérifie la lecture du courant."""
        manager = self._create_manager(current_val=250.0)
        self.assertEqual(manager.getCurrent(), 250.0)

    def test_get_current_exception(self):
        """Vérifie que getCurrent retourne None en cas d'erreur."""
        manager = self._create_manager()
        manager._SensorManager__inaSensor.readValue.side_effect = Exception("Erreur")
        self.assertIsNone(manager.getCurrent())

    def test_get_current_cle_manquante(self):
        """Vérifie que getCurrent retourne None si la clé 'Current' est absente."""
        manager = self._create_manager()
        manager._SensorManager__inaSensor.readValue.return_value = {"BusVoltage": 5.0}
        self.assertIsNone(manager.getCurrent())

    def test_gpio_lock_existe(self):
        """Vérifie que le verrou GPIO est initialisé."""
        from SensorManager import SensorManager
        manager = SensorManager(MagicMock())
        lock = manager._SensorManager__gpio_lock
        self.assertTrue(hasattr(lock, 'acquire'))
        self.assertTrue(hasattr(lock, 'release'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
