import json
import os

DATA_FILE = "player_data.json"

class GameData:
    balance = 0
    level = 1
    forest_level = 1
    brokerage_balance = 0
    stocks = {}
    stock_prices = {}
    check_value = None 

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
            cls.forest_level = data.get("forest_level", 1)
            cls.brokerage_balance = data.get("brokerage_balance", 0)
            cls.stocks = data.get("stocks", {})
            cls.stock_prices = data.get(
                "stock_prices", {"negr_bank": 1000, "mine": 3000}
            )
            cls.check_value = data.get("check_value")

            cls.verify_data()

        except Exception:
            cls.reset_data()
            cls.save()

    @classmethod
    def save(cls):
        cls.update_check_value()
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "balance": cls.balance,
                    "level": cls.level,
                    "forest_level": cls.forest_level,
                    "brokerage_balance": cls.brokerage_balance,
                    "stocks": cls.stocks,
                    "stock_prices": cls.stock_prices,
                    "check_value": cls.check_value
                },
                file,
                indent=4,
                ensure_ascii=False
            )

    @classmethod
    def reset_data(cls):
        """reset player data ;)"""
        cls.balance = 0
        cls.level = 1
        cls.forest_level = 1
        cls.brokerage_balance = 0
        cls.stocks = {}
        cls.stock_prices = {"negr_bank": 1000, "mine": 3000}
        cls.check_value = None

    # ------------------------ Новый функционал ------------------------

    @classmethod
    def update_check_value(cls):
        total = 0

        # sum all
        total += cls.balance
        total += cls.level
        total += cls.forest_level
        total += cls.brokerage_balance
        total += sum(cls.stocks.values())
        total += sum(cls.stock_prices.values())

        cls.check_value = total * 8 - 1

    @classmethod
    def verify_data(cls):
        """"Check control value"""
        total = 0
        total += cls.balance
        total += cls.level
        total += cls.forest_level
        total += cls.brokerage_balance
        total += sum(cls.stocks.values())
        total += sum(cls.stock_prices.values())

        calculated = total * 8 - 1

        if cls.check_value != calculated:
            cls.reset_data()
            cls.save()
