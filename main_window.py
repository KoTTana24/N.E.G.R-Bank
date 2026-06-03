from PySide6 import QtWidgets, QtCore
from translate import Translate
from style import Style
from game_data import GameData

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tapping Game")
        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.menu_button = QtWidgets.QPushButton(
        Translate.ru_eng("В меню", "Menu")
        )

        self.menu_button.clicked.connect(self.back_to_menu)
        self.balance_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.level_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        self.tap_button = QtWidgets.QPushButton(Translate.ru_eng("Нажми!", "Click!"))
        self.tap_button.clicked.connect(self.tap)
        
        self.layout.addWidget(self.menu_button)
        self.layout.addWidget(self.balance_label)
        self.layout.addWidget(self.level_label)
        self.layout.addWidget(self.tap_button)

        Style.style(self)
        self.update_ui()
        
    def back_to_menu(self):
        from main_menu import MainMenu

        self.menu = MainMenu()
        self.menu.show()
        self.close()

    def tap(self):
        # Добавляем очки к балансу
        GameData.balance += GameData.level

        # Проверяем возможность повышения уровня
        threshold = GameData.level * 100
        if GameData.balance >= threshold:
            GameData.balance -= threshold
            GameData.level += 1

        # Сохраняем прогресс
        GameData.save()
        self.update_ui()

    def update_ui(self):
        self.balance_label.setText(
            Translate.ru_eng(f"Баланс: {GameData.balance}", f"Balance: {GameData.balance}")
        )
        self.level_label.setText(
            Translate.ru_eng(f"Уровень: {GameData.level}", f"Level: {GameData.level}")
        )
