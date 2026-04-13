import time
import logging
import threading
import busio
from MotorManager import MotorManager
from SensorManager import SensorManager
from logs_config import setup_logging

setup_logging()

OBSTACLE_THRESHOLD = 30
SAFE_DISTANCE = 45
AVOIDANCE_STEERING = 70
EMERGENCY_DISTANCE = 8
SPEED_MAX = 40
SPEED_MIN = 15
SPEED_CRUISE = 25


class Car:

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
        self.logger.info("--- Diagnostic moteurs DC ---")
        self.__motorManager.setSpeed(0)
        time.sleep(0.5)
        self.__motorManager.setSpeed(25)
        time.sleep(0.25)
        self.__motorManager.setSpeed(0)
        time.sleep(0.25)
        self.__motorManager.setSpeed(-25)
        time.sleep(0.25)
        self.__motorManager.setSpeed(0)
        self.logger.info("Moteurs DC : OK")

        self.logger.info("--- Diagnostic servomoteur ---")
        self.__motorManager.setAngle(0)
        time.sleep(0.5)
        self.__motorManager.setAngle(100)
        time.sleep(1)
        self.__motorManager.setAngle(0)
        time.sleep(1)
        self.__motorManager.setAngle(-100)
        time.sleep(1)
        self.__motorManager.setAngle(0)
        self.logger.info("Servomoteur : OK")

    def prepareSensors(self) -> bool:
        self.logger.info("--- Diagnostic capteurs ---")
        all_ready = True

        try:
            data_rgb = self.__sensorManager._SensorManager__rgbSensor.readValue()
            if data_rgb is not None:
                self.logger.info(f"RGB : R={data_rgb.red} G={data_rgb.green} B={data_rgb.blue}")
            else:
                raise ValueError("Valeur None")
        except Exception as e:
            self.logger.error(f"Capteur RGB : ÉCHEC — {e}")
            all_ready = False

        try:
            current = self.__sensorManager.getCurrent()
            if current is not None:
                self.logger.info(f"INA219 : Courant = {current} mA")
            else:
                raise ValueError("Valeur None")
        except Exception as e:
            self.logger.error(f"Capteur INA219 : ÉCHEC — {e}")
            all_ready = False

        try:
            dist = self.__sensorManager.getDistance()
            if dist is not None:
                self.logger.info(f"Distances : F={dist.front} L={dist.left} R={dist.right}")
            else:
                raise ValueError("Valeur None")
        except Exception as e:
            self.logger.error(f"Capteurs distance : ÉCHEC — {e}")
            all_ready = False

        try:
            line = self.__sensorManager.detectLine()
            self.logger.info(f"Capteur ligne : {'détectée' if line else 'pas de ligne'}")
        except Exception as e:
            self.logger.error(f"Capteur ligne : ÉCHEC — {e}")
            all_ready = False

        if all_ready:
            self.logger.info("=== DIAGNOSTIC : TOUS LES CAPTEURS OK ===")
        else:
            self.logger.warning("=== DIAGNOSTIC : CERTAINS CAPTEURS EN ÉCHEC ===")

        return all_ready

    def startCar(self):
        self.logger.info("Démarrage progressif — marche avant")
        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(15)
        time.sleep(1)
        self.__motorManager.setSpeed(25)
        time.sleep(1)
        self.__motorManager.setSpeed(35)
        time.sleep(1)
        self.__motorManager.setSpeed(45)
        time.sleep(1)
        self.__motorManager.setSpeed(55)
        time.sleep(1)

        self.__motorManager.setSpeed(0)
        self.logger.info("Arrêt")
        time.sleep(1)

        self.logger.info("Démarrage progressif — marche arrière")
        self.__motorManager.setSpeed(-15)
        time.sleep(1)
        self.__motorManager.setSpeed(-25)
        time.sleep(1)
        self.__motorManager.setSpeed(-35)
        time.sleep(1)
        self.__motorManager.setSpeed(-45)
        time.sleep(1)
        self.__motorManager.setSpeed(-55)
        time.sleep(1)

        self.__motorManager.setSpeed(0)
        self.logger.info("Démarrage progressif terminé")

    def stopCar(self):
        self.__motorManager.setSpeed(0)
        self.__motorManager.setAngle(0)
        self.logger.info("Véhicule arrêté")

    def uTurn(self):
        self.logger.info("Début demi-tour")

        self.__motorManager.setAngle(-100)
        self.__motorManager.setSpeed(35)
        time.sleep(1.2)

        self.__motorManager.setSpeed(0)
        time.sleep(1.5)
        self.__motorManager.setAngle(100)
        self.__motorManager.setSpeed(-35)
        time.sleep(1.2)

        self.__motorManager.setSpeed(0)
        time.sleep(1.5)
        self.__motorManager.setAngle(-100)
        self.__motorManager.setSpeed(50)
        time.sleep(1.2)

        self.__motorManager.setSpeed(0)
        self.__motorManager.setAngle(0)
        self.logger.info("Demi-tour terminé")

    def figureEight(self):
        self.logger.info("Début figure en 8")

        self.__motorManager.setSpeed(-30)
        time.sleep(0.5)
        self.__motorManager.setSpeed(-60)
        self.__motorManager.setAngle(-56)

        time.sleep(4.38)

        self.__motorManager.setAngle(60)
        time.sleep(4.78)

        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(0)
        self.logger.info("Figure en 8 terminée")

    def reverseGear(self):
        self.logger.info("Marche arrière")
        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(-SPEED_MIN)
        time.sleep(1.5)
        self.__motorManager.setSpeed(0)
        self.logger.info("Marche arrière terminée")

    def zigzagAvoidance(self):
        self.logger.info("Évitement obstacle détecté")

        dist = self.__sensorManager.getDistance()
        front = dist.front if dist.front is not None else SAFE_DISTANCE
        left = dist.left if dist.left is not None else 0
        right = dist.right if dist.right is not None else 0

        if front <= EMERGENCY_DISTANCE:
            self.logger.warning(f"URGENCE : obstacle à {front} cm — arrêt immédiat")
            self.__motorManager.setSpeed(0)
            self.__motorManager.setAngle(0)
            return

        self.__motorManager.setSpeed(SPEED_MIN)

        if left >= right:
            steer_avoid = -AVOIDANCE_STEERING
            steer_return = AVOIDANCE_STEERING
        else:
            steer_avoid = AVOIDANCE_STEERING
            steer_return = -AVOIDANCE_STEERING

        self.__motorManager.setAngle(steer_avoid)
        self.__motorManager.setSpeed(SPEED_CRUISE)
        time.sleep(1.2)

        self.__motorManager.setAngle(steer_return)
        self.__motorManager.setSpeed(SPEED_CRUISE)
        time.sleep(1.0)

        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(SPEED_CRUISE)
        time.sleep(0.5)

        self.logger.info("Obstacle évité")

    def lineCount(self):
        with self.__lock:
            current_state = self.__sensorManager.detectLine()

            if current_state and not self.__last_line_state:
                self.__tour += 1
                if self.__tour == 0:
                    self.logger.info("=== LIGNE DE DÉPART FRANCHIE ===")
                else:
                    self.logger.info(f"=== TOUR {self.__tour}/{self.__totalLaps} TERMINÉ ===")

            self.__last_line_state = current_state
            return self.__tour

    def testLineSensor(self, timeout: float = 5.0):
        self.logger.info(f"Test capteur de ligne : max {timeout}s...")
        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(SPEED_MIN)

        try:
            start = time.monotonic()
            while time.monotonic() - start < timeout:
                if self.__sensorManager.detectLine():
                    self.logger.info("Ligne noire détectée — arrêt")
                    self.stopCar()
                    return True
                time.sleep(0.05)
            self.logger.info("Timeout — aucune ligne détectée")
            self.stopCar()
            return False
        except KeyboardInterrupt:
            self.stopCar()
            self.logger.info("Test capteur de ligne interrompu")
            return False

    def getDistanceReadings(self):
        return self.__sensorManager.getDistance()

    def setSpeed(self, speed):
        self.__motorManager.setSpeed(speed)

    def setAngle(self, angle):
        self.__motorManager.setAngle(angle)

    def computeSteering(self, left, right):
        if left + right == 0:
            return 0
        deviation = (right - left) / (left + right)
        steering = int(deviation * AVOIDANCE_STEERING)
        return max(-100, min(100, steering))

    def modeEvitement(self):
        self.logger.info("Mode évitement d'obstacles activé")
        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(SPEED_CRUISE)

        try:
            while True:
                dist = self.__sensorManager.getDistance()
                front = dist.front if dist.front is not None else 100.0
                left = dist.left if dist.left is not None else 0.0
                right = dist.right if dist.right is not None else 0.0

                if front <= EMERGENCY_DISTANCE:
                    self.__motorManager.setSpeed(0)
                    self.__motorManager.setAngle(0)
                    while True:
                        time.sleep(0.05)
                        dist = self.__sensorManager.getDistance()
                        f = dist.front if dist.front is not None else 100.0
                        if f > OBSTACLE_THRESHOLD:
                            self.__motorManager.setSpeed(SPEED_CRUISE)
                            self.__motorManager.setAngle(0)
                            break
                elif front <= OBSTACLE_THRESHOLD:
                    if left >= right:
                        self.__motorManager.setAngle(-AVOIDANCE_STEERING)
                    else:
                        self.__motorManager.setAngle(AVOIDANCE_STEERING)
                    self.__motorManager.setSpeed(SPEED_MIN)
                else:
                    self.__motorManager.setAngle(0)
                    self.__motorManager.setSpeed(SPEED_CRUISE)

                time.sleep(0.02)
        except KeyboardInterrupt:
            self.logger.info("Évitement interrompu")
        finally:
            self.stopCar()

    def modeTourner(self):
        self.logger.info("Mode suivi de couloir activé")
        self.__motorManager.setAngle(0)

        try:
            while True:
                speed, steering = self.stayMid()
                self.__motorManager.setAngle(steering)
                self.__motorManager.setSpeed(speed)

                if speed == 0 and steering == 0:
                    while True:
                        time.sleep(0.05)
                        dist = self.__sensorManager.getDistance()
                        f = dist.front if dist.front is not None else 100.0
                        if f > OBSTACLE_THRESHOLD:
                            break

                time.sleep(0.02)
        except KeyboardInterrupt:
            self.logger.info("Suivi de couloir interrompu")
        finally:
            self.stopCar()

    def stayMid(self) -> tuple:
        dist = self.__sensorManager.getDistance()
        front = dist.front if dist.front is not None else 100.0
        left = dist.left if dist.left is not None else 0.0
        right = dist.right if dist.right is not None else 0.0

        if front <= EMERGENCY_DISTANCE:
            self.logger.warning(f"stayMid : obstacle à {front} cm — arrêt")
            return (0, 0)

        steering = self.computeSteering(left, right)

        if front <= OBSTACLE_THRESHOLD:
            speed = SPEED_MIN
        else:
            speed = SPEED_CRUISE

        return (speed, steering)

    def start(self, max_tours: int) -> None:
        if not isinstance(max_tours, int) or max_tours < 1:
            raise ValueError("max_tours doit être un entier >= 1.")

        self.__totalLaps = max_tours
        self.__tour = -1
        self.__last_line_state = False
        self.logger.info(f"=== DÉPART COURSE : {max_tours} tour(s) ===")

        self.__motorManager.setAngle(0)

        try:
            while True:
                speed, steering = self.stayMid()

                self.__motorManager.setAngle(steering)
                self.__motorManager.setSpeed(speed)

                if speed == 0 and steering == 0:
                    while True:
                        time.sleep(0.05)
                        dist = self.__sensorManager.getDistance()
                        f = dist.front if dist.front is not None else 100.0
                        if f > OBSTACLE_THRESHOLD:
                            break

                current_lap = self.lineCount()

                if current_lap >= max_tours:
                    self.logger.info(
                        f"=== COURSE TERMINÉE : {max_tours} tour(s) complété(s) ==="
                    )
                    break

                time.sleep(0.02)

        except KeyboardInterrupt:
            self.logger.info("Course interrompue par l'utilisateur")
        finally:
            self.stopCar()
