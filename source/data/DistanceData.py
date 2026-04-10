class DistanceData:
    """
    Classe de données pour stocker les distances mesurées par les capteurs ultrasoniques.

    Attributs:
        __front (float): Distance avant en cm (None si indisponible).
        __left (float): Distance gauche en cm (None si indisponible).
        __right (float): Distance droite en cm (None si indisponible).
    """

    def __init__(self, front: float, left: float, right: float):
        for name, value in [("front", front), ("left", left), ("right", right)]:
            if value is not None:
                if not isinstance(value, (int, float)):
                    raise ValueError(f"{name} doit être un nombre ou None.")
                if value < 0:
                    raise ValueError(f"{name} ne peut pas être négatif.")

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
