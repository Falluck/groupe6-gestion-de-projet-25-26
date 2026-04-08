from LineSensor import LineSensor
from DistanceSensor import DistanceSensor
from RGBSensor import RGBSensor
from INASensor import INASensor
from data.DistanceData import DistanceData
import threading
import busio


class SensorManager:
    """Gestionnaire de tous les capteurs du véhicule."""

    def __init__(self, i2c_bus: busio.I2C):
        self.__lineSensor = LineSensor(20)
        self.__distSensorFront = DistanceSensor(6, 5, "Front")
        self.__distSensorLeft = DistanceSensor(11, 9, "Left")
        self.__distSensorRight = DistanceSensor(26, 19, "Right")
        self.__rgbSensor = RGBSensor(i2c_bus)
        self.__inaSensor = INASensor(i2c_bus)
        self.__gpio_lock = threading.Lock()

    def detectLine(self) -> bool:
        """Détecte si le véhicule est sur une ligne noire."""
        pass

    def getDistance(self) -> DistanceData:
        """Récupère les distances des trois capteurs ultrasoniques."""
        pass

    def isGreen(self, greenMinimum: int = 25, deltaMinimum: int = 5) -> bool:
        """Détecte si la couleur captée est verte."""
        pass

    def isRed(self, redMinimum: int = 150, deltaMinimum: int = 30) -> bool:
        """Détecte si la couleur captée est rouge."""
        pass

    def getCurrent(self) -> float:
        """Récupère le courant mesuré par le capteur INA219."""
        pass