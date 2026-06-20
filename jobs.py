from PySide6 import QtWidgets, QtCore

from translate import Translate
from style import Style
from game import Game


# ---------------- JOB MENU ----------------
class JobsMenu(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel(
            Translate.ru_eng("Выберите работу", "Choose job"),
            alignment=QtCore.Qt.AlignCenter
        )

        self.layout.addWidget(self.label)

        Style.style(self)

        self.modes = [
            {
                "ru": "Лесоруб",
                "en": "Lumberjack",
                "class": Lumberjack,
                "level": 5
            }
        ]

        for mode in self.modes:

            btn = QtWidgets.QPushButton(
                Translate.ru_eng(mode["ru"], mode["en"])
            )

            btn.clicked.connect(
                lambda _, m=mode: self.open_mode(m["class"], m["level"])
            )

            self.layout.addWidget(btn)

    def open_mode(self, window_class, min_level):

        if Game.level.value < min_level:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                Translate.ru_eng(
                    f"Нужен уровень {min_level}",
                    f"Level {min_level} required"
                )
            )
            return

        self.mode_window = window_class()
        self.mode_window.show()
        self.close()


# ---------------- LUMBERJACK ----------------
class Lumberjack(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.tree_hp = 5
        self.tree_felled_count = 0

        self.layout = QtWidgets.QVBoxLayout(self)

        self.menu_button = QtWidgets.QPushButton(
            Translate.ru_eng("В меню", "Menu")
        )

        self.chop_button = QtWidgets.QPushButton(
            Translate.ru_eng("Рубить дерево", "Chop tree")
        )

        self.status = QtWidgets.QLabel(
            alignment=QtCore.Qt.AlignCenter
        )

        self.menu_button.clicked.connect(self.back_to_menu)
        self.chop_button.clicked.connect(self.chop)

        self.layout.addWidget(self.menu_button)
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.chop_button)

        Style.style(self)
        self.update_ui()

    # ---------------- CHOP ----------------
    def chop(self):

        self.tree_hp -= 1

        if self.tree_hp <= 0:

            self.tree_hp = 25
            self.tree_felled_count += 1

            
            Game.balance.value += (
                Game.level.value *
                Game.forest.level.value *
                2
            )

            self.upgrade_level()
            Game.save()

        self.update_ui()

    # ---------------- LEVEL UP ----------------
    def upgrade_level(self):

        if self.tree_felled_count >= 10:

            Game.forest.level.value += 1
            self.tree_felled_count = 0

            Game.save()

    # ---------------- UI ----------------
    def update_ui(self):

        self.status.setText(
            Translate.ru_eng(
                f"Лесоруб: {Game.forest.level.value}\n"
                f"Баланс: {Game.balance.value}\n"
                f"Опыт: {self.tree_felled_count}/10",

                f"Lumberjack: {Game.forest.level.value}\n"
                f"Balance: {Game.balance.value}\n"
                f"XP: {self.tree_felled_count}/10"
            )
        )

    # ---------------- MENU ----------------
    def back_to_menu(self):

        from main_menu import MainMenu

        self.menu = MainMenu()
        self.menu.show()
        self.close()
