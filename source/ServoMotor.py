class ServoMotor:
    """
    Représentation d'un servomoteur de direction.
    Attributs:
        __boardChannel (int): Canal sur le driver PCA9685.
        __rangeDegrees (int): Amplitude maximale de rotation en degrés.
        __centerAngle (int): Angle central du servo (position neutre).
        __frequency (int): Fréquence PWM en Hz.
        __minPulse (float): Largeur d'impulsion minimale en ms.
        __maxPulse (float): Largeur d'impulsion maximale en ms.
    """

    def __init__(self, boardChannel: int, rangeDegrees: int):
        self.__boardChannel = boardChannel
        self.__rangeDegrees = rangeDegrees
        self.__centerAngle = 80
        self.__frequency = 50
        self.__minPulse = 1.0
        self.__maxPulse = 2.0

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
    def minPulse(self) -> float:
        return self.__minPulse

    @property
    def maxPulse(self) -> float:
        return self.__maxPulse
