import time
import logging
import threading
import busio
from MotorManager import MotorManager
from SensorManager import SensorManager
from logs_config import setup_logging

setup_logging()


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
        self.__motorManager.setAngle(50)
        time.sleep(1)
        self.__motorManager.setAngle(0)
        time.sleep(1)
        self.__motorManager.setAngle(-50)
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
        Démarre la voiture en augmentant progressivement la vitesse
        pour éviter une accélération brutale.
        """
        self.logger.info("Démarrage progressif")
        self.__motorManager.setSpeed(25)
        time.sleep(1)
        self.__motorManager.setSpeed(50)
        time.sleep(1)
        self.__motorManager.setSpeed(75)

    def stopCar(self):
        """Arrête la voiture (vitesse et direction à zéro)."""
        self.__motorManager.setSpeed(0)
        self.__motorManager.setAngle(0)
        self.logger.info("Véhicule arrêté")

    def uTurn(self):
        """
        Effectue un demi-tour en manœuvrant avant/arrière avec braquage.
        4 cycles de recul/avance avec braquage alterné.
        """
        self.logger.info("Début demi-tour")

        for _ in range(4):
            self.__motorManager.setAngle(-100)
            self.__motorManager.setSpeed(-25)
            time.sleep(1)
            self.__motorManager.setAngle(20)
            self.__motorManager.setSpeed(10)
            time.sleep(1)

        self.__motorManager.setAngle(0)
        self.__motorManager.setSpeed(40)
        time.sleep(1)
        self.__motorManager.setSpeed(0)
        self.logger.info("Demi-tour terminé")
