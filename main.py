import sys
from PySide6 import QtCore, QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.player_balance = 0
        self.player_level = 1

        self.balance_text = QtWidgets.QLabel(
            f"Your balance is {self.player_balance}", alignment=QtCore.Qt.AlignCenter
        )
        self.balance_plus_button = QtWidgets.QPushButton("Click me!")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.balance_text)
        self.layout.addWidget(self.balance_plus_button)

        self.balance_plus_button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.player_balance += self.player_level
        self.balance_text.setText(f"Your balance is {self.player_balance}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.resize(400, 300)
    widget.show()
    sys.exit(app.exec())
