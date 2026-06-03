import sys
from PySide6 import QtWidgets, QtCore
from translate import Translate
from style import Style
from main_window import MainWindow 

class WelcomeWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.main_text = QtWidgets.QLabel("Welcome. Добро пожаловать", alignment=QtCore.Qt.AlignCenter)
        self.choice_languege_text = QtWidgets.QLabel(
            "Choose the language. Выберите язык", alignment=QtCore.Qt.AlignCenter
        )

        self.ru_lang_button = QtWidgets.QPushButton("Russian / Русский")
        self.en_lang_button = QtWidgets.QPushButton("English / English")

        Style.style(self)

        self.ru_lang_button.clicked.connect(self.set_languege_ru)
        self.en_lang_button.clicked.connect(self.set_languege_en)

        self.layout.addWidget(self.main_text)
        self.layout.addWidget(self.choice_languege_text)
        self.layout.addWidget(self.ru_lang_button)
        self.layout.addWidget(self.en_lang_button)

    def set_languege_ru(self):
        with open('locale.txt', 'w', encoding='utf-8') as f:
            f.write('ru')
        self.open_main_window()

    def set_languege_en(self):
        with open('locale.txt', 'w', encoding='utf-8') as f:
            f.write('en')

        self.open_main_window()

    def open_main_window(self):
        self.main_window = MainWindow() 
        self.main_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = WelcomeScreen()
    widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec())
