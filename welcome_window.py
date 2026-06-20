from PySide6 import QtWidgets, QtCore
from translate import Translate
from style import Style

class WelcomeWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("N.E.G.R Bank")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel(
            "Welcome! / Добро пожаловать!",
            alignment=QtCore.Qt.AlignCenter
        )
        self.lang_label = QtWidgets.QLabel(
            "Choose the language / Выберите язык",
            alignment=QtCore.Qt.AlignCenter
        )
        Style.style(self)

        self.ru_button = QtWidgets.QPushButton("Русский / Russian")
        self.en_button = QtWidgets.QPushButton("English / Английский")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lang_label)
        self.layout.addWidget(self.ru_button)
        self.layout.addWidget(self.en_button)

        self.ru_button.clicked.connect(self.set_ru)
        self.en_button.clicked.connect(self.set_en)

    def set_ru(self):
        with open('locale.txt', 'w', encoding='utf-8') as f:
            f.write('ru')

        self.open_main_menu()

    def set_en(self):
        with open('locale.txt', 'w', encoding='utf-8') as f:
            f.write('en')

        self.open_main_menu()

    def open_main_menu(self):
        from main_menu import MainMenu  
        self.menu = MainMenu()
        self.menu.show()
        self.close()
