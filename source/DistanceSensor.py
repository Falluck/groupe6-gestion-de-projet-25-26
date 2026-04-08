import RPi.GPIO as GPIO
import time
from Sensor import Sensor


class DistanceSensor(Sensor):
    """Capteur de distance ultrasonique (HC-SR04)."""

    def __init__(self, pinTrig: int, pinEcho: int, side: str):
        self.__pinTrig = pinTrig
        self.__pinEcho = pinEcho
        self.__side = side.capitalize()

        GPIO.setup(self.__pinTrig, GPIO.OUT)
        GPIO.setup(self.__pinEcho, GPIO.IN)

    @property
    def side(self) -> str:
        return self.__side

    def readValue(self) -> float:
        """Mesure la distance via le capteur ultrasonique."""
        pass
