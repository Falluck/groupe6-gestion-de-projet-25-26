import logging
import os


def setup_logging(log_dir="logs", log_file="car.log"):
    """
    Configure le système de logs automatique.
    Les logs sont écrits dans un fichier ET affichés dans la console.

    Args:
        log_dir (str): Répertoire des fichiers de log.
        log_file (str): Nom du fichier de log.
    """
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
