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
        """Détecte si le véhicule est sur une ligne noire."""
        try:
            return self.__lineSensor.readValue()
        except Exception as e:
            print(f"Erreur lors de la détection de ligne : {e}")
            return False

    def getDistance(self) -> DistanceData:
        """
        Récupère les distances des trois capteurs ultrasoniques en parallèle.
        Chaque capteur est lu dans un thread séparé.
        """
        results = [None, None, None]

        def read_sensor(index, sensor):
            readings = []
            for _ in range(2):
                with self.__gpio_lock:
                    value = sensor.readValue()
                if value is not None:
                    readings.append(value)
            results[index] = round(sum(readings) / len(readings), 1) if readings else None

        sensors = [
            (0, self.__distSensorFront),
            (1, self.__distSensorLeft),
            (2, self.__distSensorRight),
        ]

        threads = []
        for index, sensor in sensors:
            t = threading.Thread(target=read_sensor, args=(index, sensor))
            t.start()
            threads.append(t)

        for t in threads:
            t.join(timeout=1.0)

        return DistanceData(results[0], results[1], results[2])

    def isGreen(self, greenMinimum: int = 25, deltaMinimum: int = 5) -> bool:
        """Détecte si la couleur captée est verte."""
        try:
            data = self.__rgbSensor.readValue()
            return data.green >= greenMinimum and (data.green - data.red) >= deltaMinimum
        except Exception as e:
            print(f"Erreur lors de la détection du vert : {e}")
            return False

    def isRed(self, redMinimum: int = 150, deltaMinimum: int = 30) -> bool:
        """Détecte si la couleur captée est rouge."""
        try:
            data = self.__rgbSensor.readValue()
            return data.red >= redMinimum and (data.red - data.green) >= deltaMinimum
        except Exception as e:
            print(f"Erreur lors de la détection du rouge : {e}")
            return False

    def getCurrent(self) -> float:
        """Récupère le courant mesuré par le capteur INA219."""
        try:
            sensor_data = self.__inaSensor.readValue()
            return sensor_data.get("Current", None)
        except Exception as e:
            print(f"Erreur lors de la lecture du courant : {e}")
            return None
