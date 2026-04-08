from I2CSensor import I2CSensor
from data.RGBData import RGBData
import adafruit_tcs34725


class RGBSensor(I2CSensor):
    """Capteur de couleur RGB (TCS34725) via I2C."""

    def __init__(self, i2c_bus):
        super().__init__(i2c_bus)
        self.__sensor = adafruit_tcs34725.TCS34725(self._i2c_bus)

    def readValue(self) -> RGBData:
        """Lit les valeurs RGB du capteur."""
        pass
