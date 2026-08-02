from qfluentwidgets import (
    FluentWindow,
    FluentIcon as fi,
    Theme,
    setTheme,
    setThemeColor
)

from .pages.dashboard import Dashboard


class Momentum(FluentWindow):
    def __init__(self, logic, async_helper, color_theme):
        super().__init__()

        self.logic = logic
        self.async_helper = async_helper
        self.color_theme = color_theme

        self.dashboard = Dashboard(self)

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
        event.accept()