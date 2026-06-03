class Style:
    def style(self):
        gruvbox_black = "#282828"
        gruvbox_blue = "#83a598"
        gruvbox_cyan = "#8ec07c"
        gruvbox_green = "#b8bb26"
        gruvbox_magenta = "#d3869b"
        gruvbox_red = "#fb4934"
        gruvbox_white = "#d5c4a1"
        gruvbox_yellow = "#fabd2f"
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {gruvbox_white};
                color: {gruvbox_white};
            }}

            QPushButton {{
                background-color: {gruvbox_yellow};
                color: {gruvbox_black};
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }}

            QPushButton:pressed {{
                background-color: {gruvbox_green};
            }}

            QLineEdit {{
                background-color: {gruvbox_white};
                color: {gruvbox_black};
                border: 2px solid 83ab98;
                border-radius: 8px;
                padding: 5px;
            }}

            QLabel {{
                color: {gruvbox_black};
                font-size: 18px;
            }}
        """)
