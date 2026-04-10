import time
import busio
import board
import RPi.GPIO as GPIO
from Car import Car


def afficher_menu():
    """Affiche le menu principal."""
    print("\n" + "=" * 50)
    print("        MENU PRINCIPAL — VOITURE AUTONOME")
    print("=" * 50)
    print("  [1]  Diagnostic moteurs")
    print("  [2]  Diagnostic capteurs")
    print("  [3]  Diagnostic complet")
    print("  [4]  Démarrage progressif")
    print("  [5]  Demi-tour")
    print("  [6]  Quitter")
    print("=" * 50)


def mode_diagnostic_moteurs(car):
    """Teste les moteurs DC et le servo."""
    print("Test moteurs en cours...")
    car.prepareMotors()
    print("Terminé.")


def mode_diagnostic_capteurs(car):
    """Teste tous les capteurs."""
    print("Test capteurs en cours...")
    all_ok = car.prepareSensors()
    if all_ok:
        print("RÉSULTAT : Tous les capteurs OK.")
    else:
        print("RÉSULTAT : Certains capteurs en échec.")


def mode_diagnostic_complet(car):
    """Teste moteurs + capteurs."""
    print("=" * 50)
    print("        DIAGNOSTIC PRE-COURSE")
    print("=" * 50)

    print("\n--- Test moteurs ---")
    car.prepareMotors()
    time.sleep(1)

    print("\n--- Test capteurs ---")
    all_ok = car.prepareSensors()
    time.sleep(1)

    print()
    if all_ok:
        print("RÉSULTAT : Tout est OK, la voiture est prête.")
    else:
        print("RÉSULTAT : Certains capteurs sont en échec. Vérifiez le câblage.")


def main():
    """Point d'entrée principal."""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    i2c_bus = busio.I2C(board.SCL, board.SDA)
    car = Car(i2c_bus)

    actions = {
        "1": ("Diagnostic moteurs", lambda: mode_diagnostic_moteurs(car)),
        "2": ("Diagnostic capteurs", lambda: mode_diagnostic_capteurs(car)),
        "3": ("Diagnostic complet", lambda: mode_diagnostic_complet(car)),
        "4": ("Démarrage progressif", lambda: car.startCar()),
        "5": ("Demi-tour", lambda: car.uTurn()),
    }

    try:
        while True:
            afficher_menu()
            choix = input("Choix : ").strip()

            if choix == "6":
                print("Arrêt du programme.")
                break

            action = actions.get(choix)
            if action:
                print(f"\n--- {action[0]} ---")
                action[1]()
            else:
                print("Choix invalide. Tapez un chiffre entre 1 et 6.")

    except KeyboardInterrupt:
        print("\nArrêt de la voiture.")
    finally:
        car.stopCar()
        GPIO.cleanup()
        print("GPIO nettoyé. Au revoir !")


if __name__ == "__main__":
    main()