from PySide6 import QtWidgets, QtCore
from translate import Translate
from style import Style
from game_data import GameData
from main_window import MainWindow

class Jobs(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.tree_hp = 5 # to cut down the tree player need chop tree 5 times
        self.tree_felled_count = 0

        self.layout = QtWidgets.QVBoxLayout(self)
        self.menu_button = QtWidgets.QPushButton(
            Translate.ru_eng("В меню", "Menu")
        )
        self.chop_button = QtWidgets.QPushButton(
            Translate.ru_eng("Рубить дерево", "Chop tree")
        )
        self.status = QtWidgets.QLabel(
            Translate.ru_eng(
                f"""Ваш уровень лесоруба: {GameData.forest_level}
                Ваш баланс: {GameData.balance}
                Опыт: {self.tree_felled_count}/10""",
                f"""Your lumberjack level is {GameData.forest_level}
                Your bank level: {GameData.balance}
                Experience: {self.tree_felled_count}"""
            ),
            alignment=QtCore.Qt.AlignCenter
        )
        Style.style(self)

        self.menu_button.clicked.connect(self.back_to_menu)
        self.chop_button.clicked.connect(self.chop)

        self.layout.addWidget(self.menu_button)
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.chop_button)

    def chop(self):
        self.tree_hp -= 1

        if self.tree_hp <= 0:

            self.tree_hp = 5

            self.tree_felled_count += 1

            GameData.balance += (
                GameData.level *
                GameData.forest_level *
                10
            )

            self.upgrade_level()

            GameData.save()

        self.update_ui()


    def upgrade_level(self):
        if self.tree_felled_count >= 10:
            GameData.forest_level += 1
            self.tree_felled_count = 0


    def back_to_menu(self):
        from main_menu import MainMenu

        self.menu = MainMenu()
        self.menu.show()
        self.close()


    def update_ui(self):
        self.status.setText(
            Translate.ru_eng(
                f"""Ваш уровень лесоруба: {GameData.forest_level}
                Ваш баланс: {GameData.balance}
                Опыт: {self.tree_felled_count}/10""",
                f"""Your lumberjack level is {GameData.forest_level}
                Your bank balance: {GameData.balance}
                Experience: {self.tree_felled_count}/10"""
            )
        )


