import RPi.GPIO as GPIO
import time
from Sensor import Sensor


class LineSensor(Sensor):
    """Capteur infrarouge de détection de ligne."""

    def __init__(self, pinGPIO: int):
        self.__pinGPIO = pinGPIO
        GPIO.setup(self.__pinGPIO, GPIO.IN)

    @property
    def pinGPIO(self) -> int:
        return self.__pinGPIO

    def readValue(self) -> bool:
        """Lit la valeur du capteur de ligne."""
        pass

