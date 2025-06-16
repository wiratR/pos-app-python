import sys
import os
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox
from route import load_view

def setup_logging():
    """Create logs directory and configure logging."""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(log_dir, "app.log"),
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

def main():
    setup_logging()
    logging.info("🚀 Application started")

    try:
        app = QApplication(sys.argv)
        window = load_view("home")
        window.show()

        exit_code = app.exec()
        logging.info("✅ Application exited with code %d", exit_code)
        sys.exit(exit_code)

    except Exception as e:
        logging.exception("❌ An error occurred during app startup")
        QMessageBox.critical(None, "Startup Error", f"An error occurred:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
