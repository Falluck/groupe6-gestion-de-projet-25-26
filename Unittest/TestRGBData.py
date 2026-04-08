import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from data.RGBData import RGBData


class TestRGBData(unittest.TestCase):
    """Tests pour la classe RGBData."""

    def test_creation_valeurs_normales(self):
        """Vérifie la création avec des valeurs RGB normales."""
        data = RGBData(120, 200, 50)
        self.assertEqual(data.red, 120)
        self.assertEqual(data.green, 200)
        self.assertEqual(data.blue, 50)

    def test_creation_valeurs_zero(self):
        """Vérifie la création avec des zéros (noir)."""
        data = RGBData(0, 0, 0)
        self.assertEqual(data.red, 0)
        self.assertEqual(data.green, 0)
        self.assertEqual(data.blue, 0)

    def test_creation_valeurs_max(self):
        """Vérifie la création avec des valeurs max (blanc)."""
        data = RGBData(255, 255, 255)
        self.assertEqual(data.red, 255)
        self.assertEqual(data.green, 255)
        self.assertEqual(data.blue, 255)

    def test_proprietes_lecture_seule(self):
        """Vérifie que les propriétés sont en lecture seule."""
        data = RGBData(100, 100, 100)
        with self.assertRaises(AttributeError):
            data.red = 0
        with self.assertRaises(AttributeError):
            data.green = 0
        with self.assertRaises(AttributeError):
            data.blue = 0


if __name__ == '__main__':
    unittest.main()
