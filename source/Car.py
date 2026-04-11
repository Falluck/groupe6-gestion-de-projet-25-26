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
    """
    Classe principale du véhicule autonome.
    Orchestre les managers de capteurs et de moteurs pour piloter la voiture.

    Attributs:
        __carName (str): Nom du véhicule.
        __sensorManager (SensorManager): Gestionnaire des capteurs.
        __motorManager (MotorManager): Gestionnaire des moteurs.
        __tour (int): Compteur de tours actuel.
        __totalLaps (int): Nombre total de tours à effectuer.
        __lock (RLock): Verrou pour la synchronisation des threads.
        __last_line_state (bool): Dernier état du capteur de ligne.
    """

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
        """
        Teste les moteurs DC et le servomoteur avant la course.
        Vérifie que chaque moteur répond correctement en effectuant
        un cycle avant/arrière pour les DC et gauche/droite pour le servo.
        """
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
        """
        Teste individuellement chaque capteur et génère un diagnostic automatique.

        Returns:
            bool: True si tous les capteurs répondent, False sinon.
        """
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
        """
        Démarre la voiture en avançant 5 secondes de plus en plus vite,
        s'arrête, puis fait de même en marche arrière.
        """
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
        """Arrête la voiture (vitesse et direction à zéro)."""
        self.__motorManager.setSpeed(0)
        self.__motorManager.setAngle(0)
        self.logger.info("Véhicule arrêté")

    def uTurn(self):
        """
        Effectue un demi-tour en 3 étapes :
        1. Avance + braque à gauche
        2. Recule + braque à droite
        3. Avance + braque à gauche
        """
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
        """
        La voiture roule en dessinant un 8 au sol.
        Boucle gauche puis boucle droite, retour au point de départ.
        """
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
            """
            Marche arrière à vitesse réduite pendant 1.5 secondes puis arrêt.
            Utilisé pour reculer avant un demi-tour ou après un obstacle.
            """
            self.logger.info("Marche arrière")
            self.__motorManager.setAngle(0)
            self.__motorManager.setSpeed(-SPEED_MIN)
            time.sleep(1.5)
            self.__motorManager.setSpeed(0)
            self.logger.info("Marche arrière terminée")
            
    def zigzagAvoidance(self):
        """
        Évite un obstacle détecté devant la voiture.
        Compare les distances gauche et droite, braque du côté dégagé,
        dépasse l'obstacle, puis revient au centre.
        """
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

    def getDistanceReadings(self):
        """
        Lit les capteurs de distance une fois et retourne les résultats.

        Returns:
            DistanceData: Les distances front, left, right.
        """
        return self.__sensorManager.getDistance()

    def setSpeed(self, speed):
        """Envoie une consigne de vitesse aux moteurs."""
        self.__motorManager.setSpeed(speed)

    def setAngle(self, angle):
        """Envoie une consigne de braquage au servo."""
        self.__motorManager.setAngle(angle)

    def computeSteering(self, left, right):
        """
        Calcule l angle de braquage proportionnel à la différence gauche/droite.
        Plus un mur est proche, plus la voiture braque dans le sens opposé.

        Args:
            left (float): Distance gauche en cm.
            right (float): Distance droite en cm.

        Returns:
            int: Angle de braquage (-100 à 100).
        """
        if left + right == 0:
            return 0
        deviation = (right - left) / (left + right)
        steering = int(deviation * AVOIDANCE_STEERING)
        return max(-100, min(100, steering))
