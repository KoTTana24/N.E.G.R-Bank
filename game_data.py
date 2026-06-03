import json
import os

DATA_FILE = "player_data.json"

class GameData:
    balance = 0
    level = 1

    @classmethod
    def load(cls):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cls.balance = data.get("balance", 0)
                    cls.level = data.get("level", 1)
            except Exception:
                cls.balance = 0
                cls.level = 1
        else:
            cls.save()  # создаём файл, если нет

    @classmethod
    def save(cls):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "balance": cls.balance,
                "level": cls.level
            }, f)
