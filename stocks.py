import random
from PySide6 import QtWidgets, QtCore

from translate import Translate
from style import Style
from game import Game
from game_data import GameData


class Stocks(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stocks")

        self.stocks_data = {
            "negr_bank": {"ru": "Н.Е.Г.Р Банк", "en": "N.E.G.R Bank"},
            "mine": {"ru": "Шахта", "en": "Mine"}
        }

        self.layout = QtWidgets.QVBoxLayout(self)

        # MENU
        self.menu_button = QtWidgets.QPushButton(
            Translate.ru_eng("В меню", "Menu")
        )



        self.menu_button.clicked.connect(self.back_to_menu)
        self.layout.addWidget(self.menu_button)

        # DEPOSIT / WITHDRAW
        self.deposit_button = QtWidgets.QPushButton(
            Translate.ru_eng("Пополнить брокерский счёт", "Deposit")
        )
        self.withdraw_button = QtWidgets.QPushButton(
            Translate.ru_eng("Вывести на основной счёт", "Withdraw")
        )

        self.deposit_button.clicked.connect(self.deposit)
        self.withdraw_button.clicked.connect(self.withdraw)
        
        self.layout.addWidget(self.deposit_button)
        self.layout.addWidget(self.withdraw_button)


        # BALANCE LABEL
        self.balance_label = QtWidgets.QLabel()
        self.layout.addWidget(self.balance_label)

        # PORTFOLIO 
        self.portfolio_button = QtWidgets.QPushButton(
            Translate.ru_eng("Портфель", "Portfolio")
        )

        self.portfolio_button.clicked.connect(self.show_portfolio)

        self.layout.addWidget(self.portfolio_button)

        # STOCK BUTTONS
        self.stock_buttons = {}
        for stock_id in self.stocks_data:
            btn = QtWidgets.QPushButton()
            btn.clicked.connect(lambda _, sid=stock_id: self.buy_stock(sid))
            self.stock_buttons[stock_id] = btn
            self.layout.addWidget(btn)
        
        Style.style(self)

        # TIMERS
        self.price_timer = QtCore.QTimer()
        self.price_timer.timeout.connect(self.change_prices)
        self.price_timer.start(60000)

        self.dividend_timer = QtCore.QTimer()
        self.dividend_timer.timeout.connect(self.pay_dividends)
        self.dividend_timer.start(300000)

        self.update_ui()

    # ---------------- UI ----------------
    def update_ui(self):

        self.balance_label.setText(
            Translate.ru_eng(
                f"Брокерский баланс: {Game.brokerage.value}",
                f"Brokerage balance: {Game.brokerage.value}"
            )
        )

        for stock_id, btn in self.stock_buttons.items():
            price = Game.stock_price.value.get(stock_id, 1000)

            name = Translate.ru_eng(
                self.stocks_data[stock_id]["ru"],
                self.stocks_data[stock_id]["en"]
            )

            btn.setText(f"{name}: {price}")

    def show_portfolio(self):

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(Translate.ru_eng("Портфель", "Portfolio"))

        layout = QtWidgets.QVBoxLayout(dialog)

        info_label = QtWidgets.QLabel()
        layout.addWidget(info_label)

        buttons_container = QtWidgets.QVBoxLayout()
        layout.addLayout(buttons_container)

        def refresh():
            # очистка кнопок
            while buttons_container.count():
                item = buttons_container.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # обновление текста
            lines = []

            for stock_id in self.stocks_data:

                amount = GameData.get(f"stocks.owned.{stock_id}")

                if amount <= 0:
                    continue

                name = Translate.ru_eng(
                    self.stocks_data[stock_id]["ru"],
                    self.stocks_data[stock_id]["en"]
                )

                lines.append(f"{name}: {amount}")

                btn = QtWidgets.QPushButton(f"Sell 1 {name}")

                btn.clicked.connect(
                    lambda _, sid=stock_id: (self.sell_stock(sid), refresh())
                )

                buttons_container.addWidget(btn)

            info_label.setText("\n".join(lines) if lines else "Empty portfolio")

        refresh()

        dialog.exec()
    # ---------------- BUY ----------------
    def buy_stock(self, stock_id):

        price = Game.stock_price.value.get(stock_id, 1000)
        total = int(price * 1.05)

        if Game.brokerage.value < total:
            return

        Game.brokerage.value -= total

        owned = Game.stock_owned.value.get(stock_id, 0)
        Game.stock_owned.value[stock_id] = owned + 1

        Game.stock_owned.value = Game.stock_owned.value  # save trigger
        Game.save()
        self.update_ui()

    # ---------------- SELL ----------------
    def sell_stock(self, stock_id):

        owned = Game.stock_owned.value.get(stock_id, 0)
        if owned <= 0:
            return

        price = Game.stock_price.value.get(stock_id, 1000)
        income = int(price * 0.95)

        Game.brokerage.value += income
        Game.stock_owned.value[stock_id] = owned - 1

        Game.save()
        self.update_ui()

    # ---------------- DEPOSIT ----------------
    def deposit(self):

        amount, ok = QtWidgets.QInputDialog.getInt(
            self,
            "Deposit",
            f"Balance: {Game.balance.value}",
            0, 0, Game.balance.value
        )

        if ok and amount > 0:

            Game.balance.value -= amount
            Game.brokerage.value += amount

            Game.save()
            self.update_ui()

    # ---------------- WITHDRAW ----------------
    def withdraw(self):

        amount, ok = QtWidgets.QInputDialog.getInt(
            self,
            "Withdraw",
            "Amount:",
            0, 0, Game.brokerage.value
        )

        if ok and amount > 0:

            Game.balance.value += amount
            Game.brokerage.value -= amount

            Game.save()
            self.update_ui()

    # ---------------- PRICE CHANGE ----------------
    def change_prices(self):

        for stock_id in self.stocks_data:

            price = Game.stock_price.value.get(stock_id, 1000)
            change = random.randint(1, 5)

            if random.choice([True, False]):
                price *= 1 + change / 100
            else:
                price *= 1 - change / 100

            Game.stock_price.value[stock_id] = max(1, round(price))

        Game.save()
        self.update_ui()

    # ---------------- DIVIDENDS ----------------
    def pay_dividends(self):

        total = 0

        for stock_id in self.stocks_data:

            amount = Game.stock_owned.value.get(stock_id, 0)
            price = Game.stock_price.value.get(stock_id, 1000)

            total += price * amount * 0.01

        Game.brokerage.value += int(total)

        Game.save()
        self.update_ui()

    # ---------------- MENU ----------------
    def back_to_menu(self):
        from main_menu import MainMenu

        self.menu = MainMenu()
        self.menu.show()
        self.close()
