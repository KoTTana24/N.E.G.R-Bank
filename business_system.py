from PySide6 import QtCore
from game_data import GameData
from ui_manager import UIManager


class BusinessSystem(QtCore.QObject):
    def __init__(self):
        super().__init__()
        UIManager.register(self)

        self.businesses = {}

    def register(self, business_id, business_class):
        self.businesses[business_id] = business_class

    def open(self, business_id):
        if business_id in self.businesses:
            return self.businesses[business_id]()

        return None
