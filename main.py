import sys
from translate import Translate
from style import Style
from PySide6 import QtCore, QtWidgets

class MainWindow(QtWidgets.QWidget):
    
    def __init__(self):

        super().__init__()
        self.player_balance = 0
        self.player_level = 1

        self.main_text = QtWidgets.QLabel(Translate.ru_eng(f"Ваш баланс {self.player_balance}",
            f"Your balance is {self.player_balance}"), alignment=QtCore.Qt.AlignCenter
        )
        self.main_text.setText(Translate.ru_eng(f"Ваш баланс {self.player_balance}",
            f"Your balance is {self.player_balance}"))

        self.up_level_text = QtWidgets.QLabel(Translate.ru_eng(f"Уровень пользователя: {self.player_level}",
                                                               f"Curent level is: {self.player_level}"), alignment=QtCore.Qt.AlignCenter)

        self.balance_plus_button = QtWidgets.QPushButton(Translate.ru_eng("Нажмите для получения денег!",
                                                                          "Click to get money!"))
        self.up_level_button = QtWidgets.QPushButton(Translate.ru_eng("Нажмите для улучшения уровня",
                                                                      "Click to upgrade your level"))
        Style.style(self)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.main_text)
        self.layout.addWidget(self.up_level_text)
        self.layout.addWidget(self.up_level_button)
        self.layout.addWidget(self.balance_plus_button)

        self.up_level_button.clicked.connect(self.up_level)
        self.balance_plus_button.clicked.connect(self.balance_plus)

    @QtCore.Slot()
    def balance_plus(self):
        self.player_balance += self.player_level
        self.update_ui()
    def up_level(self):
        if self.player_balance >= self.player_level * 100:
            self.player_balance -= self.player_level * 100
            self.player_level += 1
            self.main_text.setText(Translate.ru_eng("Уровень улучшен!", "Level is upgrade!"))
    
        else:
            self.main_text.setText(Translate.ru_eng("Баланс слишком маленький для улучшения",
                                                    "Balance is too small to upgrade"))

    def update_ui(self):
        self.main_text.setText(Translate.ru_eng(
        f"Ваш баланс {self.player_balance}",
        f"Your balance is {self.player_balance}"
    ))
        self.up_level_text.setText(Translate.ru_eng(
        f"Нынешний уровень {self.player_level}",
        f"Current level is {self.player_level}"
    ))



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec())


