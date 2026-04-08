class DistanceData:
    """
    Classe de données pour stocker les distances mesurées.  
    """

    def __init__(self, front: float, left: float, right: float):
        self.__front = front
        self.__left = left
        self.__right = right

    @property
    def front(self) -> float:
        return self.__front

    @property
    def left(self) -> float:
        return self.__left

    @property
    def right(self) -> float:
        return self.__right
