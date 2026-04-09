import RPi.GPIO as GPIO
import time
from Sensor import Sensor


class DistanceSensor(Sensor):
    """
    Capteur de distance ultrasonique (HC-SR04).
    Hérite de Sensor. Utilise les GPIO du Raspberry Pi.

    Attributs:
        __pinTrig (int): Numéro de broche GPIO pour le trigger.
        __pinEcho (int): Numéro de broche GPIO pour l'écho.
        __side (str): Côté du véhicule (ex: "Front", "Left", "Right").
    """

    def __init__(self, pinTrig: int, pinEcho: int, side: str):
        if not isinstance(pinTrig, int) or pinTrig < 0:
            raise ValueError("pinTrig doit être un entier positif ou nul.")
        if not isinstance(pinEcho, int) or pinEcho < 0:
            raise ValueError("pinEcho doit être un entier positif ou nul.")
        if not isinstance(side, str) or len(side.strip()) == 0:
            raise ValueError("side doit être une chaîne non vide.")

        self.__pinTrig = pinTrig
        self.__pinEcho = pinEcho
        self.__side = side.capitalize()

        GPIO.setup(self.__pinTrig, GPIO.OUT)
        GPIO.setup(self.__pinEcho, GPIO.IN)

    @property
    def side(self) -> str:
        return self.__side

    def readValue(self) -> float:
        """
        Mesure la distance via le capteur ultrasonique.

        Returns:
            float: Distance en centimètres, ou None en cas d'erreur.

        Raises:
            TimeoutError: Si le signal dépasse le délai.
            ValueError: Si la distance est hors plage (2-400 cm).
        """
        try:
            GPIO.output(self.__pinTrig, True)
            time.sleep(0.00001)
            GPIO.output(self.__pinTrig, False)

            deadline = time.time() + 0.05
            while GPIO.input(self.__pinEcho) == 0:
                if time.time() > deadline:
                    raise TimeoutError("Signal de départ trop long.")

            start_time = time.time()

            deadline = time.time() + 0.05
            while GPIO.input(self.__pinEcho) == 1:
                if time.time() > deadline:
                    raise TimeoutError("Signal de fin trop long.")

            stop_time = time.time()

            duration = stop_time - start_time
            if duration <= 0:
                raise ValueError("Durée invalide.")

            distance = round(duration * 17150, 2)

            if distance < 2 or distance > 400:
                raise ValueError(f"Distance hors plage : {distance} cm")

            return distance

        except Exception as e:
            print(f"[{self.__side}] Erreur : {e}")
            return None
