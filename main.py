import sys
from PySide6 import QtWidgets
from game_data import GameData
from welcome_window import WelcomeWindow

if __name__ == "__main__":
    GameData.load()

    app = QtWidgets.QApplication([])

    welcome = WelcomeWindow()
    welcome.show()

    sys.exit(app.exec())
