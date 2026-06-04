import json
import os

DATA_FILE = "player_data.json"


class GameData:
    balance = 0
    level = 1

    brokerage_balance = 0

    stocks = {}

    stock_prices = {
        "negr_bank": 1000,
        "mine": 3000
    }

    @classmethod
    def load(cls):
        if not os.path.exists(DATA_FILE):
            cls.save()
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            cls.balance = data.get("balance", 0)
            cls.level = data.get("level", 1)

            cls.brokerage_balance = data.get(
                "brokerage_balance",
                0
            )

            cls.stocks = data.get("stocks", {})

            cls.stock_prices = data.get(
                "stock_prices",
                {
                    "negr_bank": 1000,
                    "mine": 3000
                }
            )

        except Exception:
            cls.save()

    @classmethod
    def save(cls):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "balance": cls.balance,
                    "level": cls.level,
                    "brokerage_balance": cls.brokerage_balance,
                    "stocks": cls.stocks,
                    "stock_prices": cls.stock_prices
                },
                file,
                indent=4,
                ensure_ascii=False
            )
