import time
import busio
import board
import RPi.GPIO as GPIO
from Car import Car


def afficher_menu():
    print("\n" + "=" * 50)
    print("        MENU PRINCIPAL — VOITURE AUTONOME")
    print("=" * 50)
    print("  [1]  Diagnostic complet")
    print("  [2]  Démarrage progressif (avant + arrière)")
    print("  [3]  Demi-tour")
    print("  [4]  Figure en 8")
    print("  [5]  Évitement obstacle (conduite continue)")
    print("  [6]  Suivi de couloir (tourner)")
    print("  [7]  Test infrarouge (arrêt sur ligne noire)")
    print("  [8]  Course autonome (nombre de tours)")
    print("  [9]  Course autonome (départ au feu vert)")
    print("  [0]  Quitter")
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
                print("\n--- Diagnostic complet ---")
                car.prepareMotors()
                time.sleep(1)
                all_ok = car.prepareSensors()
                print("Tout est OK." if all_ok else "Certains capteurs en échec.")
            elif choix == "2":
                print("\n--- Démarrage progressif ---")
                car.startCar()
            elif choix == "3":
                print("\n--- Demi-tour ---")
                car.uTurn()
            elif choix == "4":
                print("\n--- Figure en 8 ---")
                car.figureEight()
            elif choix == "5":
                print("\n--- Évitement obstacle ---")
                print("(Ctrl+C pour arrêter)")
                car.modeEvitement()
            elif choix == "6":
                print("\n--- Suivi de couloir ---")
                print("(Ctrl+C pour arrêter)")
                car.modeTourner()
            elif choix == "7":
                print("\n--- Test infrarouge ---")
                print("La voiture roule 5s max ou s'arrête sur ligne noire.")
                detected = car.testLineSensor()
                print("LIGNE DÉTECTÉE !" if detected else "Pas de ligne (timeout).")
            elif choix == "8":
                print("\n--- Course autonome ---")
                try:
                    nb = int(input("Nombre de tours à effectuer : ").strip())
                    if nb < 1:
                        print("Le nombre de tours doit être >= 1.")
                    else:
                        print(f"Lancement de la course : {nb} tour(s)")
                        print("(Ctrl+C pour arrêter)")
                        car.start(nb)
                except ValueError:
                    print("Veuillez entrer un nombre entier valide.")
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

