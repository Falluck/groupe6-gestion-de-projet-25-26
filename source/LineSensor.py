import RPi.GPIO as GPIO
import time
from Sensor import Sensor


class LineSensor(Sensor):
    """
    Capteur infrarouge de détection de ligne.
    Hérite de Sensor. Utilise un GPIO du Raspberry Pi.

    Attributs:
        __pinGPIO (int): Numéro de broche GPIO.
    """

    def __init__(self, pinGPIO: int):
        if not isinstance(pinGPIO, int) or pinGPIO < 0:
            raise ValueError("pinGPIO doit être un entier positif ou nul.")

        self.__pinGPIO = pinGPIO
        GPIO.setup(self.__pinGPIO, GPIO.IN)

    @property
    def pinGPIO(self) -> int:
        return self.__pinGPIO

    def readValue(self) -> bool:
        """
        Lit la valeur du capteur de ligne.

        Returns:
            True si une ligne noire est détectée (GPIO = 0),
            False sinon (GPIO = 1).

        Raises:
            TimeoutError: Si aucune lecture stable dans le délai imparti.
        """
        start_time = time.time()
        timeout = 1.0

        while True:
            result = GPIO.input(self.__pinGPIO)
            if result == 0:
                return False
            elif result == 1:
                return True

            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout en attente d'une valeur GPIO valide")

            time.sleep(0.001)
