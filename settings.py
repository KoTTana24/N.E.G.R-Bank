from PySide6 import QtWidgets, QtCore

from translate import Translate
from style import Style
from game import Game
from ui_manager import UIManager


class Settings(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        UIManager.register(self)

        self.setWindowTitle("Settings")
        self.layout = QtWidgets.QVBoxLayout(self)

        # ---------------- MENU ----------------
        self.menu_button = QtWidgets.QPushButton(Translate.ru_eng("Меню", "Menu"))
        self.menu_button.clicked.connect(self.back_to_menu)

        # ---------------- LANGUAGE ----------------
        self.lang_label = QtWidgets.QLabel(Translate.ru_eng("Язык", "Language"))

        self.lang_ru = QtWidgets.QPushButton("Русский")
        self.lang_en = QtWidgets.QPushButton("English")

        self.lang_ru.clicked.connect(lambda: self.set_lang("ru"))
        self.lang_en.clicked.connect(lambda: self.set_lang("en"))

        # ---------------- PADDING ----------------
        self.padding_label = QtWidgets.QLabel(
            Translate.ru_eng("Толшина кнопок", "Button padding")
        )

        self.padding_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.padding_slider.setMinimum(5)
        self.padding_slider.setMaximum(50)
        self.padding_slider.setValue(Game.settings_padding.value)

        self.padding_slider.valueChanged.connect(self.change_padding)

        # ---------------- PROMO ----------------
        self.promo_input = QtWidgets.QLineEdit()
        self.promo_input.setPlaceholderText(Translate.ru_eng("Промокод", "Promocodes"))

        self.promo_btn = QtWidgets.QPushButton(
            Translate.ru_eng("Активировать", "Activate")
        )
        self.promo_btn.clicked.connect(self.use_promo)

        # ---------------- ADD UI ----------------
        self.layout.addWidget(self.menu_button)

        self.layout.addWidget(self.lang_label)
        self.layout.addWidget(self.lang_ru)
        self.layout.addWidget(self.lang_en)

        self.layout.addWidget(self.padding_label)
        self.layout.addWidget(self.padding_slider)

        self.layout.addWidget(self.promo_input)
        self.layout.addWidget(self.promo_btn)

        Style.style(self)

    # =========================================================
    # 🌍 LIVE LANGUAGE UPDATE
    # =========================================================
    def set_lang(self, lang):

        Game.language.value = lang
        Game.save()

        self.refresh_ui()  # 🔥 instant update

    def change_padding(self, value):

        Game.settings_padding.value = value
        Game.save()

        Game.signals.settings_changed.emit()

    def set_lang(self, lang):

        Game.language.value = lang
        Game.save()

        Game.signals.language_changed.emit()

    def refresh_ui(self):
        """refresh interface"""
        self.lang_label.setText(Translate.ru_eng("Язык", "Language"))
        self.padding_label.setText(Translate.ru_eng("Ширина кнопок", "Button padding"))
        self.promo_btn.setText(Translate.ru_eng("Активировать", "Activate"))
        self.menu_button.setText(Translate.ru_eng("В меню", "Menu"))

    # =========================================================
    # 📏 LIVE PADDING UPDATE
    # =========================================================
    def change_padding(self, value):

        Game.settings_padding.value = value
        Game.save()

        Style.style(self)  # 🔥 перестиливаем ВСЁ сразу

    # =========================================================
    # 🎁 ONE-TIME PROMOCODES
    # =========================================================
    def use_promo(self):

        code = self.promo_input.text().strip().lower()

        used = Game.used_promos.value or []

        # уже использован
        if code in used:
            self.promo_input.setText("")
            return

        reward = 0
        level_reward = 0

        if code == "money100":
            reward = 100

        elif code == "rich":
            reward = 1000

        elif code == "first_realese":
            reward = 10000
            level_reward = 3

        elif code == "negr":
            level_reward = 1

        else:
            return

        Game.balance.value += reward
        Game.level.value += level_reward

        used.append(code)
        Game.used_promos.value = used

        Game.save()

        self.promo_input.setText("")

        QtWidgets.QMessageBox.information(
            self,
            "Promo",
            Translate.ru_eng(
                f"+{reward} деняг +{level_reward} уровень",
                f"+{reward} money +{level_reward} level",
            ),
        )

    # =========================================================
    # MENU
    # =========================================================
    def back_to_menu(self):

        from main_menu import MainMenu

        self.menu = MainMenu()
        self.menu.show()
        self.close()
