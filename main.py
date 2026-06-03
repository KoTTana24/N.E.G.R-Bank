import sys
from translate import Translate
from PySide6 import QtCore, QtWidgets

class MainWindow(QtWidgets.QWidget):
    
    def __init__(self):

        super().__init__()
        self.player_balance = 0
        self.player_level = 1

        self.main_text = QtWidgets.QLabel(
            f"Your balance is {self.player_balance}", alignment=QtCore.Qt.AlignCenter
        )
        self.up_level_text = QtWidgets.QLabel(f"Curent level is {self.player_level}. Click to power up level", alignment=QtCore.Qt.AlignCenter
        )
        self.balance_plus_button = QtWidgets.QPushButton("Click to get money!")
        self.up_level_button = QtWidgets.QPushButton("Click to upgrade your level")
        self.style()

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
        self.main_text.setText(f"Your balance is {self.player_balance}")
    def up_level(self):
        if self.player_balance >= self.player_level * 100:
            self.player_balance -= self.player_level * 100
            self.player_level += 1
            self.up_level_text.setText(f"Curent level is {self.player_level}")
            self.main_text.setText("level is upgrade!")
        else:
            self.main_text.setText("balance is too small to upgrade")
    def style(self):
        gruvbox_black = "#282828"
        gruvbox_blue = "#83a598"
        gruvbox_cyan = "#8ec07c"
        gruvbox_green = "#b8bb26"
        gruvbox_magenta = "#d3869b"
        gruvbox_red = "#fb4934"
        gruvbox_white = "#d5c4a1"
        gruvbox_yellow = "#fabd2f"
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {gruvbox_white};
                color: {gruvbox_white};
            }}

            QPushButton {{
                background-color: {gruvbox_yellow};
                color: {gruvbox_black};
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }}

            QPushButton:pressed {{
                background-color: {gruvbox_green};
            }}

            QLineEdit {{
                background-color: {gruvbox_white};
                color: {gruvbox_black};
                border: 2px solid 83ab98;
                border-radius: 8px;
                padding: 5px;
            }}

            QLabel {{
                color: {gruvbox_black};
                font-size: 18px;
            }}
        """)




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec())


