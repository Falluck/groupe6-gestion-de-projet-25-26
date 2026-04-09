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

    def test_creation_red_negatif(self):
        """Vérifie que red négatif lève ValueError."""
        with self.assertRaises(ValueError):
            RGBData(-1, 100, 100)

    def test_creation_green_negatif(self):
        """Vérifie que green négatif lève ValueError."""
        with self.assertRaises(ValueError):
            RGBData(100, -1, 100)

    def test_creation_blue_negatif(self):
        """Vérifie que blue négatif lève ValueError."""
        with self.assertRaises(ValueError):
            RGBData(100, 100, -1)

    def test_creation_red_trop_grand(self):
        """Vérifie que red > 255 lève ValueError."""
        with self.assertRaises(ValueError):
            RGBData(256, 100, 100)

    def test_creation_green_trop_grand(self):
        """Vérifie que green > 255 lève ValueError."""
        with self.assertRaises(ValueError):
            RGBData(100, 256, 100)

    def test_creation_blue_trop_grand(self):
        """Vérifie que blue > 255 lève ValueError."""
        with self.assertRaises(ValueError):
            RGBData(100, 100, 256)

    def test_creation_red_string(self):
        """Vérifie que red string lève ValueError."""
        with self.assertRaises(ValueError):
            RGBData("rouge", 100, 100)

    def test_creation_red_none(self):
        """Vérifie que red None lève ValueError."""
        with self.assertRaises(ValueError):
            RGBData(None, 100, 100)


if __name__ == '__main__':
    unittest.main(verbosity=2)
