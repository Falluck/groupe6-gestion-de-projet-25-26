import RPi.GPIO as GPIO

class DCMotor:

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
        """
        Définit le sens de rotation du moteur.

        Args:
            direction (bool): True = marche avant, False = marche arrière.
        """
        if direction:
            GPIO.output(self.__pinInput1, GPIO.LOW)
            GPIO.output(self.__pinInput2, GPIO.HIGH)
        else:
            GPIO.output(self.__pinInput1, GPIO.HIGH)
            GPIO.output(self.__pinInput2, GPIO.LOW)

    def stop(self):
        
        GPIO.output(self.__pinInput1, GPIO.HIGH)
        GPIO.output(self.__pinInput2, GPIO.HIGH)