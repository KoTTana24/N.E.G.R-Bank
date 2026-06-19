import random
from PySide6 import QtWidgets, QtCore

from style import Style
from game import Game
from translate import Translate


class Casino(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Casino")
        self.layout = QtWidgets.QVBoxLayout(self)

        # MENU
        self.menu_button = QtWidgets.QPushButton(
            Translate.ru_eng("В меню", "Menu")
        )
        self.menu_button.clicked.connect(self.back_to_menu)

        # UI
        self.balance_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)

        self.text = QtWidgets.QLabel(
            Translate.ru_eng("Нажмите кнопку", "Press button"),
            alignment=QtCore.Qt.AlignCenter
        )

        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setPlaceholderText(
            Translate.ru_eng("Введите ставку", "Enter bet")
        )

        self.button = QtWidgets.QPushButton(
            Translate.ru_eng("Крутить", "Spin")
        )

        self.layout.addWidget(self.menu_button)
        self.layout.addWidget(self.balance_label)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.button)

        self.symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "B", "CH"]

        Style.style(self)

        self.button.clicked.connect(self.spin)

        self.update_balance()

    # ---------------- MENU ----------------
    def back_to_menu(self):

        from main_menu import MainMenu

        self.menu = MainMenu()
        self.menu.show()
        self.close()

    # ---------------- UI ----------------
    def update_balance(self):

        self.balance_label.setText(
            Translate.ru_eng(
                f"Баланс: {Game.balance.value}",
                f"Balance: {Game.balance.value}"
            )
        )

    # ---------------- SLOT ----------------
    @QtCore.Slot()
    def spin(self):

        text = self.line_edit.text()

        if not text.isdigit():
            self.text.setText(
                Translate.ru_eng("Введите число!", "Enter a number!")
            )
            return

        bet = int(text)

        # ❌ проверка баланса
        if Game.balance.value < bet:
            self.text.setText(
                Translate.ru_eng("Ставка больше баланса!", "Not enough money!")
            )
            return

        # 💸 снимаем ставку
        Game.balance.value -= bet

        # 🎰 слот
        result = random.choices(self.symbols, k=3)
        self.text.setText(" | ".join(result))

        # 💰 выигрыш
        win = bet

        for symbol in result:
            if symbol == "7":
                win *= 2
            elif symbol in ["B", "CH"]:
                win *= 1.3
            else:
                win *= 0.8

        # финальный доход
        Game.balance.value += int(win)

        Game.save()
        self.update_balance()
