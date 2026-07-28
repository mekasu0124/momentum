from qfluentwidgets import (
    FluentWindow,
    FluentIcon as fi,
    Theme,
    setTheme,
    setThemeColor
)

from .pages.dashboard import Dashboard
from .pages.tasks import Tasks

from .utils.async_helper import AsyncHelper
from .utils.color_theme import COLOR_THEME


class Momentum(FluentWindow):
    def __init__(self, logic):
        super().__init__()

        self.logic = logic
        self.color_theme = COLOR_THEME
        self.async_helper = AsyncHelper()

        self.dashboard = Dashboard(self)
        self.tasks = Tasks(self)

        self.init_navigation()
        self.apply_theme()
        self.apply_style()

    def init_navigation(self):
        self.addSubInterface(
            self.dashboard,
            fi.HOME.icon(
                color = self.color_theme['accent']
            ),
            "Dashboard"
        )

        self.addSubInterface(
            self.tasks,
            fi.PENCIL_INK.icon(
                color = self.color_theme['accent']
            ),
            "Tasks"
        )

    def apply_theme(self):
        setTheme(Theme.AUTO)
        setThemeColor(
            self.color_theme['primary']
        )

    def apply_style(self):
        self.setStyleSheet(
            f"""
                QWidget {{
                    background-color: {self.color_theme['background']};
                }}

                QLabel#page-title {{
                    font-weight: bold;
                    font-style: italic;
                    font-size: 20px;
                    color: {self.color_theme['primary']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                }}

                QScrollArea#task-list {{
                    border: 2px solid {self.color_theme['accent']};
                    border-radius: 6px;
                    background-color: {
                        self.color_theme['surface']
                    };
                }}

                QLabel#form-label {{
                    font-style: italic;
                    font-size: 14px;
                    color: {self.color_theme['text_secondary']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                }}

                QLineEdit#form-input {{
                    background-color: transparent;
                    border: none;
                    border-bottom: 2px solid {
                        self.color_theme['accent']
                    };
                    font-style: normal;
                    font-weight: normal;
                    font-size: 14px;
                    color: {self.color_theme['text_muted']};
                    outline: none;
                }}

                QLineEdit#form-input:hover {{
                    background-color: {
                        self.color_theme['surface_elevated']
                    };
                    color: {self.color_theme['text_primary']};
                    font-style: italic;
                    outline: none;
                }}

                QLineEdit#form-input:focus {{
                    background-color: {
                        self.color_theme['surface_light']
                    };
                    color: {self.color_theme['text_secondary']};
                    outline: none;
                }}

                QTextEdit#form-input {{
                    background-color: transparent;
                    border: 1px solid {self.color_theme['accent']};
                    border-radius: 5px;
                    font-style: normal;
                    font-weight: normal;
                    font-size: 14px;
                    color: {self.color_theme['text_muted']};
                    outline: none;
                }}

                QTextEdit#form-input:hover {{
                    background-color: {
                        self.color_theme['surface_elevated']
                    };
                    color: {self.color_theme['text_secondary']};
                    outline: none;
                }}

                QTextEdit#form-input:focus {{
                    background-color: {
                        self.color_theme['surface_light']
                    };
                    color: {self.color_theme['text_secondary']};
                    outline: none;
                }}

                QPushButton#form-btn {{
                    background-color: transparent;
                    border: 1px solid {self.color_theme['accent']};
                    border-radius: 6px;
                    color: {self.color_theme['text_muted']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    outline: none;
                }}

                QPushButton#form-btn:hover {{
                    background-color: {
                        self.color_theme['surface_elevated']
                    };
                    color: {self.color_theme['text_secondary']};
                    outline: none;
                }}

                QWidget#task-card {{
                    background-color: transparent;
                    border: 1px solid {
                        self.color_theme['accent']
                    };
                    border-radius: 8px;
                }}

                QLabel#card-title {{
                    font-weight: bold;
                    font-style: italic;
                    font-size: 14px;
                    color: {self.color_theme['text_primary']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    margin-top: 6px;
                }}

                QLabel#card-details {{
                    font-style: italic;
                    font-size: 11px;
                    color: {self.color_theme['text_muted']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                }}

                QTextEdit#card-content {{
                    border: 2px solid {
                        self.color_theme['text_muted']
                    };
                    border-radius: 4px;
                    padding: 8px;
                    background-color: {
                        self.color_theme['surface']
                    };
                    font-size: 11px;
                }}
            """
        )

    def closeEvent(self, event):
        self.logic.close_db_connection()
        event.accept()