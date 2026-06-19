import random
from PySide6 import QtWidgets, QtCore

from translate import Translate
from style import Style
from game import Game
from game_data import GameData


class Shop(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shop Tycoon")
        self.layout = QtWidgets.QVBoxLayout(self)

        self.products = {
            "fruits": 50,
            "vegetables": 30,
            "drinks": 20
        }

        self.ui()

        self.money_timer = QtCore.QTimer()
        self.money_timer.timeout.connect(self.generate_customers)
        self.money_timer.start(60000)

        self.salary_timer = QtCore.QTimer()
        self.salary_timer.timeout.connect(self.pay_salaries)
        self.salary_timer.start(600000)

        Style.style(self)

    # ---------------- UI ----------------
    def ui(self):
        self.balance_label = QtWidgets.QLabel()
        self.emp_label = QtWidgets.QLabel()
        
        self.menu_button = QtWidgets.QPushButton(
            Translate.ru_eng("В меню", "Menu")
        )
        
        self.menu_button.clicked.connect(self.back_to_menu)
        
        self.layout.addWidget(self.menu_button)


        self.buy_fruits = QtWidgets.QPushButton(Translate.ru_eng(
            "Купить фрукты ($50)",
            "Buy fruits ($50)"
        ))
        self.buy_veg = QtWidgets.QPushButton(Translate.ru_eng(
            "Купить овощи ($30)",
            "Buy vegetables ($30)"
        ))
        self.buy_drinks = QtWidgets.QPushButton(Translate.ru_eng(
            "Купить напитки ($20)",
            "Buy drinks ($20)"
        ))

        self.hire_btn = QtWidgets.QPushButton(Translate.ru_eng(
            "Нанять сотрудника ($1000)",
            "Hire employee ($1000)"
        ))
        self.fire_btn = QtWidgets.QPushButton(Translate.ru_eng(
            "Уволить сотрудника",
            "Fire employee"
        ))

        self.layout.addWidget(self.balance_label)
        self.layout.addWidget(self.buy_fruits)
        self.layout.addWidget(self.buy_veg)
        self.layout.addWidget(self.buy_drinks)
        self.layout.addWidget(self.emp_label)
        self.layout.addWidget(self.hire_btn)
        self.layout.addWidget(self.fire_btn)

        self.buy_fruits.clicked.connect(lambda: self.buy("fruits"))
        self.buy_veg.clicked.connect(lambda: self.buy("vegetables"))
        self.buy_drinks.clicked.connect(lambda: self.buy("drinks"))

        self.hire_btn.clicked.connect(self.hire)
        self.fire_btn.clicked.connect(self.fire)

        self.update_ui()

    # ---------------- UI UPDATE ----------------
    def update_ui(self):
        self.balance_label.setText(
            Translate.ru_eng(
                f"Баланс: {Game.balance}",
                f"Balance: {Game.balance}"
            )
        )

        self.emp_label.setText(
            Translate.ru_eng(
                f"Сотрудники: {Game.business.shop_employees}",
                f"Employees: {Game.business.shop_employees}"
            )
        )

    # ---------------- BUY ----------------
    def buy(self, product):
        price = self.products[product]

        if Game.balance.value < price:
            return

        Game.balance.value -= price

        # inventory path
        path = f"business.shop.inventory.{product}"
        current = Game.balance  # ❌ FIX ниже

        
        #current = Game.business.inventory[product]
        
        current = GameData.get(f"business.shop.inventory.{product}")
        GameData.set(f"business.shop.inventory.{product}", current + 1)

        #Game.business.inventory[product] = current + 1

        Game.save()
        self.update_ui()

    # ---------------- EMPLOYEES ----------------
    def hire(self):
        if Game.balance.value < 1000:
            return

        if Game.business.shop_employees >= 50:
            return

        Game.balance.sub(1000)
        GameData.set(
            "business.shop.employees",
            GameData.get("business.shop.employees") + 1
        )

        Game.save()
        self.update_ui()

    def fire(self):
        if Game.business.shop_employees <= 0:
            return

        Game.business.shop_employees -= 1

        Game.save()
        self.update_ui()

    # ---------------- ECONOMY ----------------
    def generate_customers(self):
        customers = random.randint(0, 10)
        income = 0

        for _ in range(customers):
            for _ in range(random.randint(1, 5)):

                product = random.choice(list(self.products.keys()))
                path = f"business.shop.inventory.{product}"

                stock = GameData.get(path)

                if stock > 0:
                    GameData.set(path, stock - 1)
                    income += self.products[product]   # 💥 ВАЖНО

        # сотрудники
        employees = GameData.get("business.shop.employees")
        income += employees * 10

        # баланс
        Game.balance.value += income

        if Game.balance.value <= 0:
            self.reset_shop()

        Game.save()
        self.update_ui()

    # ---------------- SALARIES ----------------
    def pay_salaries(self):
        salary = Game.business.shop_employees * 200

        Game.balance.value -= salary

        if Game.balance.value <= 0:
            self.reset_shop()

        Game.save()
        self.update_ui()

    # ---------------- RESET ----------------
    def reset_shop(self):
        Game.balance.value = 0

        Game.business.shop_employees = 0

        Game.business.inventory = {
            "fruits": 10,
            "vegetables": 10,
            "drinks": 10
        }

        Game.save()
        self.update_ui()
    def back_to_menu(self):
        from main_menu import MainMenu

        self.menu = MainMenu()
        self.menu.show()
        self.close()
