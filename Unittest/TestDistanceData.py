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
        """Vérifie la création avec des valeurs None."""
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

    def test_proprietes_lecture_seule(self):
        """Vérifie que les propriétés sont en lecture seule."""
        data = DistanceData(10.0, 20.0, 30.0)
        with self.assertRaises(AttributeError):
            data.front = 99.0
        with self.assertRaises(AttributeError):
            data.left = 99.0
        with self.assertRaises(AttributeError):
            data.right = 99.0


if __name__ == '__main__':
    unittest.main(verbosity=2)
