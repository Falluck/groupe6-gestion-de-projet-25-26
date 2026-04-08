import time
import logging
import threading
import busio
from MotorManager import MotorManager
from SensorManager import SensorManager
from logs_config import setup_logging

setup_logging()


class Car:
    """Classe principale du véhicule autonome."""

    def __init__(self, i2c_bus: busio.I2C):
        self.__carName = "Car"
        self.__sensorManager = SensorManager(i2c_bus)
        self.__motorManager = MotorManager(i2c_bus)
        self.__tour = -1
        self.__totalLaps = 0
        self.__lock = threading.RLock()
        self.__last_line_state = False
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialisation du véhicule '{self.__carName}'")

    def prepareMotors(self):
        """Teste les moteurs DC et le servomoteur avant la course."""
        pass

    def prepareSensors(self) -> bool:
        """Teste chaque capteur et génère un diagnostic."""
        pass

    def startCar(self):
        """Démarre la voiture progressivement."""
        pass

    def stopCar(self):
        """Arrête la voiture."""
        pass

    def uTurn(self):
        """Effectue un demi-tour."""
        pass
