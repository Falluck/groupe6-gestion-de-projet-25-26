from abc import ABC, abstractmethod


class Sensor(ABC):
    """Classe abstraite de base pour tous les capteurs."""

    @abstractmethod
    def readValue(self) -> any:
        pass
