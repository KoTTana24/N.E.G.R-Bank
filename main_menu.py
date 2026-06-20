from PySide6 import QtWidgets, QtCore
from translate import Translate
from style import Style
from game_data import GameData
from main_window import MainWindow
from casino import Casino
from stocks import Stocks
from jobs import JobsMenu
from shop import Shop
from game import Game

class MainMenu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("N.E.G.R Bank - Main Menu")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel(
            Translate.ru_eng("Выберите режим", "Choose mode"),
            alignment=QtCore.Qt.AlignCenter
        )
        self.layout.addWidget(self.label)

        Style.style(self)

        # mode : text, window class, required level 
        self.modes = [
            (Translate.ru_eng("Тапалка", "Tapping"), MainWindow, 1),
            (Translate.ru_eng("Казино", "Casino"), Casino, 3),
            (Translate.ru_eng("Работы", "Jobs"), JobsMenu, 5),
            (Translate.ru_eng("Акции","Stocks"), Stocks, 8),
            (Translate.ru_eng("Бизнес", "Bussiness"), Shop, 15)
        ]

        for text, cls, min_level in self.modes:
            button = QtWidgets.QPushButton(text)
            button.clicked.connect(lambda checked=False, cls=cls, lvl=min_level: self.open_mode(cls, lvl))
            self.layout.addWidget(button)

    def open_mode(self, window_class, min_level):
        if int(Game.level) < min_level:
            QtWidgets.QMessageBox.warning(
                self,
                Translate.ru_eng("Ошибка", "Error"),
                Translate.ru_eng(
                    f"Для этой игры нужен уровень {min_level}!",
                    f"This game requires level {min_level}!"
                )
            )
            return

        self.mode_window = window_class()
        self.mode_window.show()
        self.close()
