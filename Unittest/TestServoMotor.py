import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from ServoMotor import ServoMotor


class TestServoMotor(unittest.TestCase):
    """Tests pour la classe ServoMotor."""

    def setUp(self):
        self.servo = ServoMotor(0, 50)

    def test_creation_attributs(self):
        """Vérifie les attributs initiaux."""
        self.assertEqual(self.servo.boardChannel, 0)
        self.assertEqual(self.servo.rangeDegrees, 50)
        self.assertEqual(self.servo.centerAngle, 80)
        self.assertEqual(self.servo.frequency, 50)

    def test_proprietes_duty(self):
        """Vérifie minDuty (6%) et maxDuty (10%)."""
        self.assertEqual(self.servo.minDuty, 6.0)
        self.assertEqual(self.servo.maxDuty, 10.0)

    def test_creation_autres_valeurs(self):
        """Vérifie la création avec des paramètres différents."""
        servo2 = ServoMotor(3, 90)
        self.assertEqual(servo2.boardChannel, 3)
        self.assertEqual(servo2.rangeDegrees, 90)

    def test_proprietes_lecture_seule(self):
        """Vérifie que toutes les propriétés sont en lecture seule."""
        with self.assertRaises(AttributeError):
            self.servo.boardChannel = 5
        with self.assertRaises(AttributeError):
            self.servo.rangeDegrees = 100
        with self.assertRaises(AttributeError):
            self.servo.centerAngle = 90
        with self.assertRaises(AttributeError):
            self.servo.frequency = 60
        with self.assertRaises(AttributeError):
            self.servo.minDuty = 5.0
        with self.assertRaises(AttributeError):
            self.servo.maxDuty = 12.0

    def test_min_duty_inferieur_a_max_duty(self):
        """Vérifie que minDuty < maxDuty."""
        self.assertLess(self.servo.minDuty, self.servo.maxDuty)

    def test_creation_channel_negatif(self):
        """Vérifie que boardChannel négatif lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor(-1, 50)

    def test_creation_channel_trop_grand(self):
        """Vérifie que boardChannel > 15 lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor(16, 50)

    def test_creation_channel_string(self):
        """Vérifie que boardChannel string lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor("abc", 50)

    def test_creation_range_zero(self):
        """Vérifie que rangeDegrees = 0 lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor(0, 0)

    def test_creation_range_negatif(self):
        """Vérifie que rangeDegrees négatif lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor(0, -45)

    def test_creation_range_string(self):
        """Vérifie que rangeDegrees string lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor(0, "abc")


if __name__ == '__main__':
    unittest.main(verbosity=2)
