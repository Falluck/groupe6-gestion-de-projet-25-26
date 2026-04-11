import time
import busio
import board
import RPi.GPIO as GPIO
from Car import Car


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
    print("  [7]  Évitement obstacle")
    print("  [8]  Quitter")
    print("=" * 50)


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
                input("Placez un obstacle devant la voiture. Entrée pour lancer...")
                car.zigzagAvoidance()
            elif choix == "8":
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