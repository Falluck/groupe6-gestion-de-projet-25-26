import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from data.DistanceData import DistanceData


class TestDistanceData(unittest.TestCase):
    """Tests pour la classe DistanceData."""

    def test_creation_valeurs_normales(self):
        """Vérifie la création avec des valeurs normales."""
        data = DistanceData(25.5, 30.0, 28.3)
        self.assertEqual(data.front, 25.5)
        self.assertEqual(data.left, 30.0)
        self.assertEqual(data.right, 28.3)

    def test_creation_valeurs_none(self):
        """Vérifie la création avec des valeurs None (capteur indisponible)."""
        data = DistanceData(None, None, None)
        self.assertIsNone(data.front)
        self.assertIsNone(data.left)
        self.assertIsNone(data.right)

    def test_creation_valeurs_zero(self):
        """Vérifie la création avec des zéros."""
        data = DistanceData(0.0, 0.0, 0.0)
        self.assertEqual(data.front, 0.0)
        self.assertEqual(data.left, 0.0)
        self.assertEqual(data.right, 0.0)

    def test_creation_mixte_none_et_valeurs(self):
        """Vérifie la création avec un mix de None et de valeurs."""
        data = DistanceData(None, 20.0, None)
        self.assertIsNone(data.front)
        self.assertEqual(data.left, 20.0)
        self.assertIsNone(data.right)

    def test_proprietes_lecture_seule(self):
        """Vérifie que les propriétés sont en lecture seule."""
        data = DistanceData(10.0, 20.0, 30.0)
        with self.assertRaises(AttributeError):
            data.front = 99.0
        with self.assertRaises(AttributeError):
            data.left = 99.0
        with self.assertRaises(AttributeError):
            data.right = 99.0

    def test_creation_front_negatif(self):
        """Vérifie que front négatif lève ValueError."""
        with self.assertRaises(ValueError):
            DistanceData(-5.0, 20.0, 30.0)

    def test_creation_left_negatif(self):
        """Vérifie que left négatif lève ValueError."""
        with self.assertRaises(ValueError):
            DistanceData(10.0, -5.0, 30.0)

    def test_creation_right_negatif(self):
        """Vérifie que right négatif lève ValueError."""
        with self.assertRaises(ValueError):
            DistanceData(10.0, 20.0, -5.0)

    def test_creation_front_string(self):
        """Vérifie que front string lève ValueError."""
        with self.assertRaises(ValueError):
            DistanceData("loin", 20.0, 30.0)

    def test_creation_left_liste(self):
        """Vérifie que left liste lève ValueError."""
        with self.assertRaises(ValueError):
            DistanceData(10.0, [20.0], 30.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
