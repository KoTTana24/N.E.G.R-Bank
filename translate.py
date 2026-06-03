# translate.py

import os

class Translate:
    USER_LANG = "ru"  # язык по умолчанию

    @staticmethod
    def get_user_lang():
        
        if not os.path.exists("locale.txt"):
            with open("locale.txt", "w", encoding="utf-8") as f:
                f.write(Translate.USER_LANG)
            return Translate.USER_LANG

        try:
            with open("locale.txt", "r", encoding="utf-8") as f:
                lang = f.read().strip().lower()
                if lang in ("ru", "en"):
                    return lang
        except Exception:
            pass
        return Translate.USER_LANG

    @staticmethod
    def ru_eng(russian_text: str, english_text: str) -> str:
        lang = Translate.get_user_lang()
        return russian_text if lang == "ru" else english_text
