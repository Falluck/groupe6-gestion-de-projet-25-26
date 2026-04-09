from DCMotor import DCMotor
from ServoMotor import ServoMotor
import adafruit_pca9685
import busio
import time


class MotorManager:
    """
    Gestionnaire des moteurs du véhicule.
    Contrôle les moteurs DC de propulsion et le servomoteur de direction
    via un driver PWM PCA9685.

    Attributs:
        __dcMotorsPropulsion (DCMotor[]): Liste des moteurs DC.
        __servoDirection (ServoMotor): Servomoteur de direction.
        __pwmDriver (PCA9685): Driver PWM I2C.
    """

    def __init__(self, i2c_bus: busio.I2C):
        self.__dcMotorsPropulsion = [DCMotor(5, 19, 18), DCMotor(4, 17, 16)]
        self.__servoDirection = ServoMotor(0)
        self.__pwmDriver = adafruit_pca9685.PCA9685(i2c_bus, address=0x40)
        self.__pwmDriver.frequency = 50

    def setSpeed(self, speed: float) -> None:
        """
        Définit la vitesse des moteurs DC.

        Args:
            speed (float): Valeur entre -100 et 100.
                Positif = avant, négatif = arrière, 0 = arrêt.

        Raises:
            ValueError: Si speed n'est pas un nombre ou est hors plage.
        """
        try:
            if not isinstance(speed, (int, float)):
                raise ValueError("La vitesse doit être un nombre (int ou float).")
            if speed < -100 or speed > 100:
                raise ValueError("La vitesse doit être entre -100 et 100.")

            front = (speed >= 0)
            speed_value = abs(speed)
            dc_duty = int((speed_value / 100.0) * 65535)

            for motor in self.__dcMotorsPropulsion:
                if speed_value == 0:
                    motor.stop()
                else:
                    motor.setDirection(front)
                    self.__pwmDriver.channels[motor.pinEnable].duty_cycle = (
                        ((2 ** 16) - 1) - dc_duty
                    )
        except ValueError as e:
            print(e)

    def setAngle(self, steering: float) -> None:
        """
        Définit l'angle de braquage du servomoteur.

        Args:
            steering (float): Pourcentage de -100 (gauche) à 100 (droite), 0 = tout droit.

        Raises:
            ValueError: Si steering n'est pas un nombre ou est hors plage.
        """
        try:
            if not isinstance(steering, (int, float)):
                raise ValueError("Le braquage doit être un nombre (int ou float).")
            if steering < -100 or steering > 100:
                raise ValueError("Le braquage doit être entre -100 et 100.")

            servo_duty = self.convert_steering_to_duty(steering)
            self.__pwmDriver.channels[self.__servoDirection.boardChannel].duty_cycle = (
                ((2 ** 16) - 1) - servo_duty
            )
        except ValueError as e:
            print(e)

    def convert_steering_to_duty(self, steering: float) -> int:
        """
        Convertit un pourcentage de braquage (-100 à 100) en valeur duty_cycle 16 bits.

        Interpolation linéaire entre les rapports cycliques min et max du servo :
            -100 (gauche) → minDuty (6%)
               0 (centre) → 8%
            +100 (droite) → maxDuty (10%)

        Args:
            steering (float): Pourcentage de braquage.

        Returns:
            int: Valeur duty_cycle (0-65535).
        """
        min_duty = self.__servoDirection.minDuty / 100.0
        max_duty = self.__servoDirection.maxDuty / 100.0

        duty_fraction = min_duty + (max_duty - min_duty) * ((steering + 100) / 200.0)

        return int(duty_fraction * 65535)
