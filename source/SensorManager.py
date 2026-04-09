from LineSensor import LineSensor
from DistanceSensor import DistanceSensor
from RGBSensor import RGBSensor
from INASensor import INASensor
from data.DistanceData import DistanceData
import threading
import busio
import time


class SensorManager:
    """
    Gestionnaire de tous les capteurs du véhicule.

    Attributs:
        __lineSensor (LineSensor): Capteur infrarouge de ligne.
        __distSensorFront (DistanceSensor): Capteur de distance avant.
        __distSensorLeft (DistanceSensor): Capteur de distance gauche.
        __distSensorRight (DistanceSensor): Capteur de distance droit.
        __rgbSensor (RGBSensor): Capteur de couleur RGB.
        __inaSensor (INASensor): Capteur de courant/tension.
    """

    def __init__(self, i2c_bus: busio.I2C):
        self.__lineSensor = LineSensor(20)
        self.__distSensorFront = DistanceSensor(6, 5, "Front")
        self.__distSensorLeft = DistanceSensor(11, 9, "Left")
        self.__distSensorRight = DistanceSensor(26, 19, "Right")
        self.__rgbSensor = RGBSensor(i2c_bus)
        self.__inaSensor = INASensor(i2c_bus)
        self.__gpio_lock = threading.Lock()

    def detectLine(self) -> bool:
        """
        Détecte si le véhicule est sur une ligne noire.

        Returns:
            bool: True si une ligne est détectée, False sinon.
        """
        try:
            return self.__lineSensor.readValue()
        except Exception as e:
            print(f"Erreur lors de la détection de ligne : {e}")
            return False

    def getDistance(self) -> DistanceData:
        """
        Récupère les distances moyennes des trois capteurs ultrasoniques.
        Utilise un verrou pour sérialiser les accès GPIO.

        Returns:
            DistanceData: Objet contenant les distances avant, gauche et droite.
        """
        sensors = [
            self.__distSensorFront,
            self.__distSensorLeft,
            self.__distSensorRight,
        ]
        results = [None, None, None]

        for i, sensor in enumerate(sensors):
            readings = []
            for _ in range(5):
                with self.__gpio_lock:
                    value = sensor.readValue()
                if value is not None:
                    readings.append(value)
                time.sleep(0.01)
            results[i] = round(sum(readings) / len(readings), 1) if readings else None

        return DistanceData(results[0], results[1], results[2])

    def isGreen(self, greenMinimum: int = 25, deltaMinimum: int = 5) -> bool:
        """
        Détecte si la couleur captée est verte.

        Args:
            greenMinimum (int): Seuil minimum de vert.
            deltaMinimum (int): Écart minimum entre vert et rouge.

        Returns:
            bool: True si vert détecté, False sinon.
        """
        try:
            data = self.__rgbSensor.readValue()
            return data.green >= greenMinimum and (data.green - data.red) >= deltaMinimum
        except Exception as e:
            print(f"Erreur lors de la détection du vert : {e}")
            return False

    def isRed(self, redMinimum: int = 150, deltaMinimum: int = 30) -> bool:
        """
        Détecte si la couleur captée est rouge.

        Args:
            redMinimum (int): Seuil minimum de rouge.
            deltaMinimum (int): Écart minimum entre rouge et vert.

        Returns:
            bool: True si rouge détecté, False sinon.
        """
        try:
            data = self.__rgbSensor.readValue()
            return data.red >= redMinimum and (data.red - data.green) >= deltaMinimum
        except Exception as e:
            print(f"Erreur lors de la détection du rouge : {e}")
            return False

    def getCurrent(self) -> float:
        """
        Récupère le courant mesuré par le capteur INA219.

        Returns:
            float: Courant en milliampères, ou None si indisponible.
        """
        try:
            sensor_data = self.__inaSensor.readValue()
            return sensor_data.get("Current", None)
        except Exception as e:
            print(f"Erreur lors de la lecture du courant : {e}")
            return None
