import time
import threading
import busio
import board
import RPi.GPIO as GPIO
from Car import Car, SPEED_MIN, SPEED_CRUISE, EMERGENCY_DISTANCE, OBSTACLE_THRESHOLD, AVOIDANCE_STEERING


def afficher_menu():
    print("\n" + "=" * 50)
    print("        MENU PRINCIPAL — VOITURE AUTONOME")
    print("=" * 50)
    print("  [1]  Diagnostic moteurs")
    print("  [2]  Diagnostic capteurs")
    print("  [3]  Diagnostic complet")
    print("  [4]  Démarrage progressif (avant + arrière)")
    print("  [5]  Demi-tour")
    print("  [6]  Figure en 8")
    print("  [7]  Évitement obstacle (conduite continue)")
    print("  [8]  Tourner (suivi de couloir)")
    print("  [9]  Quitter")
    print("=" * 50)


class SensorReader:
    """Thread de lecture capteurs en arrière-plan."""

    def __init__(self, car):
        self.car = car
        self.front = 100.0
        self.left = 0.0
        self.right = 0.0
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def get(self):
        with self.lock:
            return self.front, self.left, self.right

    def _loop(self):
        while self.running:
            dist = self.car.getDistanceReadings()
            with self.lock:
                self.front = dist.front if dist.front is not None else 100.0
                self.left = dist.left if dist.left is not None else 0.0
                self.right = dist.right if dist.right is not None else 0.0


def mode_evitement_continu(car):
    """
    Conduite continue avec esquive d'obstacles.
    Arrêt d'urgence si < 8 cm, esquive si < 30 cm.
    """
    print("La voiture roule et esquive les obstacles.")
    print("(Ctrl+C pour arrêter)")

    reader = SensorReader(car)
    reader.start()

    car.setAngle(0)
    car.setSpeed(SPEED_CRUISE)

    try:
        while True:
            f, l, r = reader.get()

            if f <= EMERGENCY_DISTANCE:
                car.setSpeed(0)
                car.setAngle(0)
                while True:
                    time.sleep(0.05)
                    f, _, _ = reader.get()
                    if f > OBSTACLE_THRESHOLD:
                        car.setSpeed(SPEED_CRUISE)
                        car.setAngle(0)
                        break

            elif f <= OBSTACLE_THRESHOLD:
                if l >= r:
                    car.setAngle(-AVOIDANCE_STEERING)
                else:
                    car.setAngle(AVOIDANCE_STEERING)
                car.setSpeed(SPEED_MIN)

            else:
                car.setAngle(0)
                car.setSpeed(SPEED_CRUISE)

            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nArrêt de l'évitement.")
    finally:
        reader.stop()
        car.stopCar()


def mode_tourner(car):
    """
    Conduite continue avec correction de trajectoire.
    La voiture longe le couloir en restant au milieu.
    Braque proportionnellement vers le côté le plus dégagé.
    Freine dans les virages, accélère en ligne droite.
    """
    print("La voiture roule et suit le couloir.")
    print("(Ctrl+C pour arrêter)")

    reader = SensorReader(car)
    reader.start()

    car.setAngle(0)
    car.setSpeed(SPEED_CRUISE)

    try:
        while True:
            f, l, r = reader.get()

            if f <= EMERGENCY_DISTANCE:
                car.setSpeed(0)
                car.setAngle(0)
                while True:
                    time.sleep(0.05)
                    f, _, _ = reader.get()
                    if f > OBSTACLE_THRESHOLD:
                        break
                car.setSpeed(SPEED_CRUISE)
                car.setAngle(0)
                continue

            steering = car.computeSteering(l, r)
            car.setAngle(steering)

            if f <= OBSTACLE_THRESHOLD:
                car.setSpeed(SPEED_MIN)
            else:
                penalty = abs(steering) / 100.0
                speed = int(SPEED_CRUISE * (1.0 - 0.5 * penalty))
                speed = max(SPEED_MIN, speed)
                car.setSpeed(speed)

            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nArrêt du suivi.")
    finally:
        reader.stop()
        car.stopCar()


def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    car = Car(i2c_bus)

    try:
        while True:
            afficher_menu()
            choix = input("Choix : ").strip()

            if choix == "1":
                print("\n--- Diagnostic moteurs ---")
                car.prepareMotors()
            elif choix == "2":
                print("\n--- Diagnostic capteurs ---")
                all_ok = car.prepareSensors()
                print("Tous les capteurs OK." if all_ok else "Certains capteurs en échec.")
            elif choix == "3":
                print("\n--- Diagnostic complet ---")
                car.prepareMotors()
                time.sleep(1)
                all_ok = car.prepareSensors()
                print("Tout est OK." if all_ok else "Certains capteurs en échec.")
            elif choix == "4":
                print("\n--- Démarrage progressif ---")
                car.startCar()
            elif choix == "5":
                print("\n--- Demi-tour ---")
                car.uTurn()
            elif choix == "6":
                print("\n--- Figure en 8 ---")
                car.figureEight()
            elif choix == "7":
                print("\n--- Évitement obstacle ---")
                mode_evitement_continu(car)
            elif choix == "8":
                print("\n--- Tourner (suivi de couloir) ---")
                mode_tourner(car)
            elif choix == "9":
                print("Arrêt du programme.")
                break
            else:
                print("Choix invalide.")
    except KeyboardInterrupt:
        print("\nArrêt de la voiture.")
    finally:
        car.stopCar()
        GPIO.cleanup()
        print("GPIO nettoyé. Au revoir !")


if __name__ == "__main__":
    main()
