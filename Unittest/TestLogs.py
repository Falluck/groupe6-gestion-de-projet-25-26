import unittest
import logging
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from logs_config import setup_logging


class TestLogs(unittest.TestCase):
    """Tests pour le système de logs automatique."""

    def _cleanup_handlers(self):
        """Ferme et supprime tous les handlers du root logger."""
        root = logging.getLogger()
        for handler in root.handlers[:]:
            handler.close()
            root.removeHandler(handler)

    def setUp(self):
        self._cleanup_handlers()

    def tearDown(self):
        self._cleanup_handlers()

    def test_setup_logging_cree_le_dossier(self):
        """Vérifie que setup_logging crée le répertoire de logs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = os.path.join(tmpdir, "test_logs")
            setup_logging(log_dir=log_dir, log_file="test.log")
            self.assertTrue(os.path.isdir(log_dir))
            self._cleanup_handlers()

    def test_setup_logging_ecrit_dans_fichier(self):
        """Vérifie que les logs sont écrits dans un fichier."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = os.path.join(tmpdir, "test_logs")
            setup_logging(log_dir=log_dir, log_file="test.log")

            logger = logging.getLogger("test_write")
            logger.info("Message de test")

            log_path = os.path.join(log_dir, "test.log")
            self.assertTrue(os.path.isfile(log_path))
            with open(log_path, "r") as f:
                contenu = f.read()
            self.assertIn("Message de test", contenu)
            self._cleanup_handlers()

    def test_log_format_contient_level(self):
        """Vérifie que le format contient le niveau de log."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = os.path.join(tmpdir, "test_logs")
            setup_logging(log_dir=log_dir, log_file="test.log")

            logger = logging.getLogger("test_format")
            logger.info("Test format")

            log_path = os.path.join(log_dir, "test.log")
            with open(log_path, "r") as f:
                contenu = f.read()
            self.assertIn("[INFO]", contenu)
            self._cleanup_handlers()

    def test_log_erreur_enregistree(self):
        """Vérifie que les erreurs sont bien enregistrées."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = os.path.join(tmpdir, "test_logs")
            setup_logging(log_dir=log_dir, log_file="test.log")

            logger = logging.getLogger("test_error")
            logger.error("Capteur déconnecté")

            log_path = os.path.join(log_dir, "test.log")
            with open(log_path, "r") as f:
                contenu = f.read()
            self.assertIn("[ERROR]", contenu)
            self.assertIn("Capteur déconnecté", contenu)
            self._cleanup_handlers()


if __name__ == '__main__':
    unittest.main(verbosity=2)
