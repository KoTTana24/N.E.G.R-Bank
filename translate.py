class Translate:
    # Read languge 
    @staticmethod
    def get_user_lang():
        try:
            with open("locale.txt", "r", encoding="utf-8") as f:
                lang = f.read().strip().lower()
                if lang in ("ru", "en"):
                    return lang
        except FileNotFoundError:
            pass
        # Default languege is english
        return "en"

    @staticmethod
    def ru_eng(russian_text: str, english_text: str) -> str:
        lang = Translate.get_user_lang()
        if lang == "ru":
            return russian_text
        else:
            return english_text
