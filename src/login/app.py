from qfluentwidgets import (
    FluentWindow,
    FluentIcon as fi,
    Theme,
    setTheme,
    setThemeColor
)
from PySide6.QtCore import Signal

from .pages.dashboard import Dashboard


class LoginWindow(FluentWindow):
    # Signals for communication back to main
    new_user_requested = Signal()
    login_success = Signal()

    def __init__(self, logic, async_helper, color_theme):
        super().__init__()

        self.logic = logic
        self.async_helper = async_helper
        self.color_theme = color_theme

        self.dashboard = Dashboard(self)

        # Connect dashboard signals to window signals
        self.dashboard.launch_user_registration.connect(
            self.new_user_requested.emit)
        self.dashboard.login_success.connect(self.login_success.emit)

        self.init_navigation()
        self.apply_theme()
        self.apply_style()

    def init_navigation(self):
        self.addSubInterface(
            self.dashboard,
            fi.HOME.icon(
                color=self.color_theme['accent']
            ),
            "Dashboard"
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
            """
        )

    def closeEvent(self, event):
        if hasattr(self.logic, 'close_db_connection'):
            self.logic.close_db_connection()
        event.accept()
