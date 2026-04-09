class ServoMotor:
    """
    Représentation d'un servomoteur de direction.

    Attributs:
        __boardChannel (int): Canal sur le driver PCA9685 (0-15).
        __rangeDegrees (int): Amplitude maximale de rotation en degrés.
        __centerAngle (int): Angle central du servo (position neutre).
        __frequency (int): Fréquence PWM en Hz.
        __minDuty (float): Rapport cyclique (%) à l'angle max gauche.
        __maxDuty (float): Rapport cyclique (%) à l'angle max droite.
    """

    def __init__(self, boardChannel: int, rangeDegrees: int):
        if not isinstance(boardChannel, int) or boardChannel < 0 or boardChannel > 15:
            raise ValueError("boardChannel doit être un entier entre 0 et 15.")
        if not isinstance(rangeDegrees, int) or rangeDegrees <= 0:
            raise ValueError("rangeDegrees doit être un entier strictement positif.")

        self.__boardChannel = boardChannel
        self.__rangeDegrees = rangeDegrees
        self.__centerAngle = 80
        self.__frequency = 50
        self.__minDuty = 6.0
        self.__maxDuty = 10.0

    @property
    def boardChannel(self) -> int:
        return self.__boardChannel

    @property
    def rangeDegrees(self) -> float:
        return self.__rangeDegrees

    @property
    def centerAngle(self) -> float:
        return self.__centerAngle

    @property
    def frequency(self) -> float:
        return self.__frequency

    @property
    def minDuty(self) -> float:
        return self.__minDuty

    @property
    def maxDuty(self) -> float:
        return self.__maxDuty
