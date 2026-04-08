from DCMotor import DCMotor
from ServoMotor import ServoMotor
import adafruit_pca9685
import busio


class MotorManager:
    """Gestionnaire des moteurs du véhicule."""

    def __init__(self, i2c_bus: busio.I2C):
        self.__dcMotorsPropulsion = [DCMotor(5, 17, 18), DCMotor(4, 27, 22)]
        self.__servoDirection = ServoMotor(0, 50)
        self.__pwmDriver = adafruit_pca9685.PCA9685(i2c_bus, address=0x40)
        self.__pwmDriver.frequency = 50

    def setSpeed(self, speed: float) -> None:
        """Définit la vitesse des moteurs DC (-100 à 100)."""
        pass

    def setAngle(self, steering: float) -> None:
        """Définit l'angle de braquage du servomoteur (-100 à 100)."""
        pass

    def convert_steering_to_duty(self, steering: float) -> int:
        """Convertit un pourcentage de braquage en duty_cycle 16 bits.
        Interpolation linéaire entre minDuty (6%) et maxDuty (10%)."""
        pass
