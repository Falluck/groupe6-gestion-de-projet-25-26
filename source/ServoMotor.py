class ServoMotor:
    """Représentation d'un servomoteur de direction."""

    def __init__(self, boardChannel: int, rangeDegrees: int):
        self.__boardChannel = boardChannel
        self.__rangeDegrees = rangeDegrees
        self.__centerAngle = 80
        self.__frequency = 50
        self.__minDuty = 6.0    # 6% → butée gauche
        self.__maxDuty = 10.0   # 10% → butée droite

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
