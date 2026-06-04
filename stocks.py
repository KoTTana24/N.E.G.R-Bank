import random
from PySide6 import QtWidgets, QtCore

from translate import Translate
from style import Style
from game_data import GameData


class Stocks(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()



        self.setWindowTitle("Stocks")

        self.stocks_data = {
            "negr_bank": {
                "ru": "Н.Е.Г.Р Банк",
                "en": "N.E.G.R Bank"
            },
            "mine": {
                "ru": "Шахта",
                "en": "Mine"
            }
        }

        self.layout = QtWidgets.QVBoxLayout(self)

        # Кнопка возврата в меню
        self.menu_button = QtWidgets.QPushButton(
            Translate.ru_eng("В меню", "Menu")
        )
        self.menu_button.clicked.connect(self.back_to_menu)
        self.layout.addWidget(self.menu_button)

        # Кнопки пополнения и вывода средств
        self.deposit_button = QtWidgets.QPushButton(
            Translate.ru_eng("Пополнить брокерский счёт", "Deposit to brokerage")
        )
        self.withdraw_button = QtWidgets.QPushButton(
            Translate.ru_eng("Вывести на основной счёт", "Withdraw to main balance")
        )

        self.deposit_button.clicked.connect(self.deposit)
        self.withdraw_button.clicked.connect(self.withdraw)

        self.layout.addWidget(self.deposit_button)
        self.layout.addWidget(self.withdraw_button)

        # Баланс брокерского счёта
        self.balance_label = QtWidgets.QLabel()
        self.layout.addWidget(self.balance_label)

        # Кнопка портфеля
        self.portfolio_button = QtWidgets.QPushButton(
            Translate.ru_eng("Портфель", "Portfolio")
        )
        self.portfolio_button.clicked.connect(self.show_portfolio)
        self.layout.addWidget(self.portfolio_button)

        # Кнопки акций
        self.stock_buttons = {}
        for stock_id in self.stocks_data:
            button = QtWidgets.QPushButton()
            button.clicked.connect(
                lambda checked=False, sid=stock_id: self.buy_stock(sid)
            )
            self.stock_buttons[stock_id] = button
            self.layout.addWidget(button)

        Style.style(self)

        # Таймеры
        self.price_timer = QtCore.QTimer()
        self.price_timer.timeout.connect(self.change_prices)
        self.price_timer.start(60000)  # every minute

        self.dividend_timer = QtCore.QTimer()
        self.dividend_timer.timeout.connect(self.pay_dividends)
        self.dividend_timer.start(60000)  # every minute

        self.update_ui()

    # -------------------- UI --------------------
    def update_ui(self):
        self.balance_label.setText(
            Translate.ru_eng(
                f"Брокерский баланс: {GameData.brokerage_balance}",
                f"Brokerage balance: {GameData.brokerage_balance}"
            )
        )
        for stock_id, button in self.stock_buttons.items():
            price = GameData.stock_prices[stock_id]
            stock_name = Translate.ru_eng(
                self.stocks_data[stock_id]["ru"],
                self.stocks_data[stock_id]["en"]
            )
            button.setText(f"{stock_name}: {price}")

    # -------------------- Покупка/Продажа --------------------
    def buy_stock(self, stock_id):
        price = GameData.stock_prices[stock_id]
        total_price = int(price * 1.05)  # комиссия 5%
        if GameData.brokerage_balance < total_price:
            QtWidgets.QMessageBox.warning(
                self,
                "Error",
                Translate.ru_eng("Недостаточно денег", "Not enough money")
            )
            return
        GameData.brokerage_balance -= total_price
        GameData.stocks[stock_id] = GameData.stocks.get(stock_id, 0) + 1
        GameData.save()
        self.update_ui()

    def sell_stock(self, stock_id):
        if GameData.stocks.get(stock_id, 0) <= 0:
            return
        price = GameData.stock_prices[stock_id]
        income = int(price * 0.95)  # комиссия 5%
        GameData.brokerage_balance += income
        GameData.stocks[stock_id] -= 1
        GameData.save()
        self.update_ui()

    def show_portfolio(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(Translate.ru_eng("Портфель", "Portfolio"))
        layout = QtWidgets.QVBoxLayout(dialog)
        for stock_id, amount in GameData.stocks.items():
            if amount <= 0:
                continue
            name = Translate.ru_eng(
                self.stocks_data[stock_id]["ru"],
                self.stocks_data[stock_id]["en"]
            )
            button = QtWidgets.QPushButton(f"{name}: {amount}")
            button.clicked.connect(
                lambda checked=False, sid=stock_id, d=dialog: (self.sell_stock(sid), d.close())
            )
            layout.addWidget(button)
        dialog.exec()

    # -------------------- Пополнение/Вывод --------------------
    def deposit(self):
        amount, ok = QtWidgets.QInputDialog.getInt(
            self,
            Translate.ru_eng("Пополнить", "Deposit"),
            Translate.ru_eng(f"Ваш баланс: {GameData.balance}. Введите сумму для перевода на брокерский счёт:",
                             f"You'r balance is:{GameData.balance}. Enter amount to deposit:"),
            0, 0, GameData.balance
        )
        if ok and amount > 0:
            if amount > GameData.balance:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    Translate.ru_eng("Недостаточно средств на основном балансе", "Not enough money on main balance")
                )
                return
            GameData.balance -= amount
            GameData.brokerage_balance += amount
            GameData.save()
            self.update_ui()

    def withdraw(self):
        amount, ok = QtWidgets.QInputDialog.getInt(
            self,
            Translate.ru_eng("Вывести", "Withdraw"),
            Translate.ru_eng("Введите сумму для перевода на основной баланс:", "Enter amount to withdraw:"),
            0, 0, GameData.brokerage_balance
        )
        if ok and amount > 0:
            if amount > GameData.brokerage_balance:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    Translate.ru_eng("Недостаточно средств на брокерском счёте", "Not enough money on brokerage balance")
                )
                return
            GameData.balance += amount
            GameData.brokerage_balance -= amount
            GameData.save()
            self.update_ui()

    # -------------------- Изменение цены и дивиденды --------------------
    def change_prices(self):
        for stock_id in GameData.stock_prices:
            price = GameData.stock_prices[stock_id]
            change = random.randint(1, 5)
            if random.choice([True, False]):
                price *= 1 + change / 100
            else:
                price *= 1 - change / 100
            GameData.stock_prices[stock_id] = max(1, round(price))
        GameData.save()
        self.update_ui()

    def pay_dividends(self):
        dividends = 0
        for stock_id, amount in GameData.stocks.items():
            price = GameData.stock_prices[stock_id]
            dividends += price * amount * 0.01
        GameData.brokerage_balance += int(dividends)
        GameData.save()
        self.update_ui()

    # -------------------- Меню --------------------
    def back_to_menu(self):
        from main_menu import MainMenu
        self.menu = MainMenu()
        self.menu.show()
        self.close()
