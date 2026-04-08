from abc import abstractmethod
from Sensor import Sensor


class I2CSensor(Sensor):
    """Classe abstraite pour les capteurs communiquant via le bus I2C."""

    def __init__(self, i2c_bus):
        self._i2c_bus = i2c_bus

    @abstractmethod
    def readValue(self) -> any:
        pass
