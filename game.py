from game_data import GameData


class Value:
    def __init__(self, path):
        self.path = path

    @property
    def value(self):
        return GameData.get(self.path)

    @value.setter
    def value(self, new_value):
        GameData.set(self.path, new_value)

    def add(self, amount):
        self.value += amount

    def sub(self, amount):
        self.value -= amount

    def mul(self, amount):
        self.value *= amount

    def div(self, amount):
        self.value /= amount

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value or 0)

    def __float__(self):
        return float(self.value or 0)

    def _v(self, other):
        return self.value

    def __eq__(self, other):
        return self.value == other

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __sub__(self, other):
        return (self.value or 0) - other

    def __rsub__(self, other):
        return other - (self.value or 0)

class DictValue:
    def __init__(self, path):
        self.path = path

    def get(self, key):
        return GameData.get(f"{self.path}.{key}")

    def set(self, key, value):
        GameData.set(f"{self.path}.{key}", value)

class Forest:
    level = Value("jobs.forest_level")
    exp = Value("jobs.tree_exp")


class Stock:
    brokerage = Value("stocks.brokerage_balance")

class Business:
    shop_employees = Value("business.shop.employees")
    inventory = Value("business.shop.inventory")


class Game:

    @staticmethod
    def save():
        GameData.save()

    @staticmethod
    def load():
        GameData.load()

    balance = Value("player.balance")
    level = Value("player.level")

    brokerage = Value("stocks.brokerage_balance")  #
    
    stock_price = Value("market.stock_prices")
    stock_owned = Value("stocks.owned")

    forest = Forest()
    stock = Stock()
    business = Business()
