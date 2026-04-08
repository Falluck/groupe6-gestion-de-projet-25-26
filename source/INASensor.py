from I2CSensor import I2CSensor
import adafruit_ina219


class INASensor(I2CSensor):
    """Capteur de courant/tension INA219 via I2C."""

    def __init__(self, i2c_bus):
        super().__init__(i2c_bus)
        self.__sensor = adafruit_ina219.INA219(self._i2c_bus)

    def readValue(self) -> dict:
        """Lit les valeurs du capteur INA219."""
        pass
