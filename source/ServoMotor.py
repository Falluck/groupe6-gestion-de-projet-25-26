class ServoMotor:
    """
    Représentation d'un servomoteur de direction.

    Attributs:
        __boardChannel (int): Canal sur le driver PCA9685 (0-15).
        __minDuty (float): Rapport cyclique (%) à l'angle max gauche.
        __maxDuty (float): Rapport cyclique (%) à l'angle max droite.
    """

    def __init__(self, boardChannel: int):
        if not isinstance(boardChannel, int) or boardChannel < 0 or boardChannel > 15:
            raise ValueError("boardChannel doit être un entier entre 0 et 15.")

        self.__boardChannel = boardChannel
        self.__minDuty = 6.0
        self.__maxDuty = 10.0

    @property
    def boardChannel(self) -> int:
        return self.__boardChannel

    @property
    def minDuty(self) -> float:
        return self.__minDuty

    @property
    def maxDuty(self) -> float:
        return self.__maxDuty
