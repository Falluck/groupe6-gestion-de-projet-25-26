class RGBData:
    """
    Classe de données pour stocker les valeurs RGB d'un capteur de couleur.

    Attributs:
        __red (int): Valeur du canal rouge (0-255).
        __green (int): Valeur du canal vert (0-255).
        __blue (int): Valeur du canal bleu (0-255).
    """

    def __init__(self, red: int, green: int, blue: int):
        if not isinstance(red, int) or red < 0 or red > 255:
            raise ValueError("red doit être un entier entre 0 et 255.")
        if not isinstance(green, int) or green < 0 or green > 255:
            raise ValueError("green doit être un entier entre 0 et 255.")
        if not isinstance(blue, int) or blue < 0 or blue > 255:
            raise ValueError("blue doit être un entier entre 0 et 255.")

        self.__red = red
        self.__green = green
        self.__blue = blue

    @property
    def red(self) -> int:
        return self.__red

    @property
    def green(self) -> int:
        return self.__green

    @property
    def blue(self) -> int:
        return self.__blue
