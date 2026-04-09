from I2CSensor import I2CSensor
import adafruit_ina219


class INASensor(I2CSensor):
    """
    Capteur de courant/tension INA219 communiquant via I2C.
    Hérite de I2CSensor.

    Attributs:
        __sensor (INA219): Instance du driver INA219.
    """

    def __init__(self, i2c_bus):
        super().__init__(i2c_bus)
        self.__sensor = adafruit_ina219.INA219(self._i2c_bus)

    def readValue(self) -> dict:
        """
        Lit les valeurs du capteur INA219.

        Returns:
            dict: Dictionnaire contenant :
                - "BusVoltage" : Tension du bus en volts.
                - "ShuntVoltage" : Tension shunt en volts.
                - "Current" : Courant en milliampères.
        """
        return {
            "BusVoltage": self.__sensor.bus_voltage,
            "ShuntVoltage": self.__sensor.shunt_voltage / 1000,
            "Current": self.__sensor.current
        }
