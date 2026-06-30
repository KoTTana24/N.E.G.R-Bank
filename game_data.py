import json
import os


class GameData:
    FILE = "player_data.json"

    data = {}

    # ---------------- LOAD ----------------
    @staticmethod
    def load():

        if not os.path.exists(GameData.FILE):
            GameData.data = {}
            GameData.ensure_defaults()
            GameData.save()
            return

        with open(GameData.FILE, "r") as f:
            GameData.data = json.load(f)

        GameData.ensure_defaults()

    # ---------------- SAVE ----------------
    @staticmethod
    def save():

        with open(GameData.FILE, "w") as f:
            json.dump(GameData.data, f, indent=4)

    # ---------------- GET ----------------
    @staticmethod
    def get(path, default=None):

        keys = path.split(".")
        obj = GameData.data

        for k in keys:
            if isinstance(obj, dict) and k in obj:
                obj = obj[k]
            else:
                return default

        return obj

    # ---------------- SET ----------------
    @staticmethod
    def set(path, value):

        keys = path.split(".")
        obj = GameData.data

        for k in keys[:-1]:
            if k not in obj or not isinstance(obj[k], dict):
                obj[k] = {}
            obj = obj[k]

        obj[keys[-1]] = value

    # ---------------- DEFAULTS ----------------
    @staticmethod
    def ensure_defaults():

        defaults = {
            "player": {"balance": 1000, "level": 1},
            "stocks": {
                "brokerage_balance": 0,
                "owned": {},
                "stock_prices": {"negr_bank": 1000, "mine": 500},
            },
            "business": {
                "shop": {
                    "employees": 0,
                    "inventory": {"fruits": 10, "vegetables": 10, "drinks": 10},
                }
            },
            "settings": {"padding": 10, "language": "ru"},
            "used_promos": [],
        }

        GameData._merge_defaults(defaults, GameData.data)

    # ---------------- MERGE ----------------
    @staticmethod
    def _merge_defaults(defaults, target):

        for key, value in defaults.items():
            if key not in target:
                target[key] = value

            elif isinstance(value, dict):
                GameData._merge_defaults(value, target[key])
