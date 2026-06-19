import json
import os

DATA_FILE = "player_data.json"


class GameData:

    # =========================
    # DEFAULT STATE
    # =========================
    state = {
        "player": {
            "balance": 0,
            "level": 1
        },

        "jobs": {
            "forest_level": 1,
            "tree_exp": 0
        },

        "business": {
            "shop": {
                "opened": False,
                "employees": 0,
                "inventory": {
                    "fruits": 10,
                    "vegetables": 10,
                    "drinks": 10
                }
            }
        },

        "stocks": {
            "brokerage_balance": 0,
            "owned": {}
        },

        "market": {
            "stock_prices": {
                "negr_bank": 1000,
                "mine": 3000
            }
        }
    }

    # =========================
    # LOAD
    # =========================
    @classmethod
    def load(cls):
        if not os.path.exists(DATA_FILE):
            cls.save()
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                cls.state = json.load(f)

        except Exception:
            cls.state = {}
            cls.save()

        cls.ensure_defaults()

    # =========================
    # SAVE
    # =========================
    @classmethod
    def save(cls):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(cls.state, f, indent=4, ensure_ascii=False)

    # =========================
    # SAFE GET
    # =========================
    @classmethod
    def get(cls, path, default=0):
        keys = path.split(".")
        value = cls.state

        try:
            for k in keys:
                value = value[k]
            return value
        except Exception:
            return default

    # =========================
    # SAFE SET
    # =========================
    @classmethod
    def set(cls, path, value):
        keys = path.split(".")
        obj = cls.state

        for k in keys[:-1]:
            obj = obj.setdefault(k, {})

        obj[keys[-1]] = value

    # =========================
    # DEFAULT FIX (ВАЖНО)
    # =========================
    @classmethod
    def ensure_defaults(cls):

        # PLAYER
        cls.state.setdefault("player", {})
        cls.state["player"].setdefault("balance", 0)
        cls.state["player"].setdefault("level", 1)

        # JOBS
        cls.state.setdefault("jobs", {})
        cls.state["jobs"].setdefault("forest_level", 1)
        cls.state["jobs"].setdefault("tree_exp", 0)

        # BUSINESS
        cls.state.setdefault("business", {})
        cls.state["business"].setdefault("shop", {})
        shop = cls.state["business"]["shop"]

        shop.setdefault("opened", False)
        shop.setdefault("employees", 0)
        shop.setdefault("inventory", {
            "fruits": 10,
            "vegetables": 10,
            "drinks": 10
        })

        # STOCKS
        cls.state.setdefault("stocks", {})
        cls.state["stocks"].setdefault("brokerage_balance", 0)
        cls.state["stocks"].setdefault("owned", {})

        # MARKET
        cls.state.setdefault("market", {})
        cls.state["market"].setdefault("stock_prices", {
            "negr_bank": 1000,
            "mine": 3000
        })
