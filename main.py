import sys
from PySide6 import QtWidgets
from translate import Translate
from welcome_window_ui import WelcomeWindow
from main_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Создаём экран приветствия
    welcome_window = WelcomeWindow()
    welcome_window.show()

    sys.exit(app.exec())
