import RPi.GPIO as GPIO


class DCMotor:
    """Contrôle d'un moteur DC via un pont en H."""

    def __init__(self, enable: int, input1: int, input2: int):
        self.__pinEnable = enable
        self.__pinInput1 = input1
        self.__pinInput2 = input2

        GPIO.setup(self.__pinEnable, GPIO.OUT)
        GPIO.setup(self.__pinInput1, GPIO.OUT)
        GPIO.setup(self.__pinInput2, GPIO.OUT)

    @property
    def pinEnable(self) -> int:
        return self.__pinEnable

    @property
    def pinInput1(self) -> int:
        return self.__pinInput1

    @property
    def pinInput2(self) -> int:
        return self.__pinInput2

    def setDirection(self, direction: bool):
        """Définit le sens de rotation du moteur."""
        pass

    def stop(self):
        """Arrête le moteur (freinage)."""
        pass
