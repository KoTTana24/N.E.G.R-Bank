from game import Game


class UIManager:
    windows = []

    @staticmethod
    def register(window):
        UIManager.windows.append(window)

        # автоматически подключаем сигналы
        if hasattr(window, "refresh_ui"):
            Game.signals.language_changed.connect(window.refresh_ui)
            Game.signals.settings_changed.connect(window.refresh_ui)

    @staticmethod
    def refresh_all():
        for w in UIManager.windows:
            if hasattr(w, "refresh_ui"):
                w.refresh_ui()
