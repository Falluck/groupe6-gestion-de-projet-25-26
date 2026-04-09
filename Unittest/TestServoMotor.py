import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from ServoMotor import ServoMotor


class TestServoMotor(unittest.TestCase):
    """Tests pour la classe ServoMotor."""

    def setUp(self):
        self.servo = ServoMotor(0)

    def test_creation_attributs(self):
        """Vérifie les attributs initiaux."""
        self.assertEqual(self.servo.boardChannel, 0)
        self.assertEqual(self.servo.minDuty, 6.0)
        self.assertEqual(self.servo.maxDuty, 10.0)

    def test_creation_autre_channel(self):
        """Vérifie la création avec un canal différent."""
        servo2 = ServoMotor(3)
        self.assertEqual(servo2.boardChannel, 3)

    def test_min_duty_inferieur_a_max_duty(self):
        """Vérifie que minDuty < maxDuty."""
        self.assertLess(self.servo.minDuty, self.servo.maxDuty)

    def test_proprietes_lecture_seule(self):
        """Vérifie que toutes les propriétés sont en lecture seule."""
        with self.assertRaises(AttributeError):
            self.servo.boardChannel = 5
        with self.assertRaises(AttributeError):
            self.servo.minDuty = 5.0
        with self.assertRaises(AttributeError):
            self.servo.maxDuty = 12.0

    def test_creation_channel_negatif(self):
        """Vérifie que boardChannel négatif lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor(-1)

    def test_creation_channel_trop_grand(self):
        """Vérifie que boardChannel > 15 lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor(16)

    def test_creation_channel_string(self):
        """Vérifie que boardChannel string lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor("abc")

    def test_creation_channel_float(self):
        """Vérifie que boardChannel float lève ValueError."""
        with self.assertRaises(ValueError):
            ServoMotor(1.5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
