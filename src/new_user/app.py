from qfluentwidgets import (
    FluentWindow,
    FluentIcon as fi,
    Theme,
    setTheme,
    setThemeColor
)
from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QGraphicsOpacityEffect

from .pages.welcome import Welcome
from .pages.tos import TOS
from .pages.ua import UA
from .pages.register import Register


class NewUser(FluentWindow):
    login_requested = Signal()
    registration_success = Signal()

    def __init__(self, logic, async_helper, color_theme):
        super().__init__()

        self.logic = logic
        self.async_helper = async_helper
        self.color_theme = color_theme

        self.pages = []
        self.current_index = 0
        self.navigation_interfaces = []
        self.is_animating = False

        self.welcome = Welcome(self)
        self.tos = TOS(self)
        self.ua = UA(self)
        self.register = Register(self)

        self.pages.append(self.welcome)
        self.pages.append(self.tos)
        self.pages.append(self.ua)
        self.pages.append(self.register)

        self.welcome.launch_user_login.connect(
            self.login_requested.emit
        )
        self.welcome.next_page_signal.connect(
            self.next_page
        )

        self.tos.prev_page_signal.connect(
            self.prev_page
        )
        self.tos.next_page_signal.connect(
            self.next_page
        )

        self.ua.prev_page_signal.connect(
            self.prev_page
        )

        self.ua.next_page_signal.connect(
            self.next_page
        )

        self.register.registration_success.connect(
            self.registration_success.emit
        )
        self.register.prev_page_signal.connect(
            self.prev_page
        )

        self.init_navigation()
        self.apply_theme()
        self.apply_style()
        self.update_navigation_access()

    def init_navigation(self):
        welcome_interface = self.addSubInterface(
            self.welcome,
            fi.HOME.icon(
                color=self.color_theme['accent']
            ),
            "Welcome"
        )
        self.navigation_interfaces.append(welcome_interface)

        tos_interface = self.addSubInterface(
            self.tos,
            fi.DOCUMENT.icon(
                color=self.color_theme['accent']
            ),
            "TOS"
        )
        self.navigation_interfaces.append(tos_interface)

        ua_interface = self.addSubInterface(
            self.ua,
            fi.CONSTRACT.icon(
                color=self.color_theme['accent']
            ),
            "UA"
        )
        self.navigation_interfaces.append(ua_interface)

        register_interface = self.addSubInterface(
            self.register,
            fi.PENCIL_INK.icon(
                color=self.color_theme['accent']
            ),
            "Register"
        )
        self.navigation_interfaces.append(register_interface)

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

                QLabel#welcome-title {{
                    font-weight: bold;
                    font-size: 28px;
                    color: {self.color_theme['primary']};
                    letter-spacing: 0.05em;
                    background-color: transparent;
                }}
            """
        )

    def update_navigation_access(self):
        for i, interface in enumerate(self.navigation_interfaces):
            interface.setEnabled(i == self.current_index)

    def next_page(self):
        if self.current_index < len(self.pages) - 1 and not self.is_animating:
            self.is_animating = True
            current = self.pages[self.current_index]
            next_page = self.pages[self.current_index + 1]

            effect = QGraphicsOpacityEffect(current)
            current.setGraphicsEffect(effect)
            effect.setOpacity(1.0)

            QTimer.singleShot(50, lambda: effect.setOpacity(0.0))
            QTimer.singleShot(200, lambda: self.switchTo(next_page))
            QTimer.singleShot(250, lambda: effect.setOpacity(1.0))
            QTimer.singleShot(350, lambda: self.finish_transition(next_page))

    def prev_page(self):
        if self.current_index > 0 and not self.is_animating:
            self.is_animating = True
            current = self.pages[self.current_index]
            prev_page = self.pages[self.current_index - 1]

            effect = QGraphicsOpacityEffect(current)
            current.setGraphicsEffect(effect)
            effect.setOpacity(1.0)

            QTimer.singleShot(50, lambda: effect.setOpacity(0.0))
            QTimer.singleShot(200, lambda: self.switchTo(prev_page))
            QTimer.singleShot(250, lambda: effect.setOpacity(1.0))
            QTimer.singleShot(350, lambda: self.finish_transition(prev_page))

    def finish_transition(self, target_page):
        self.current_index = self.pages.index(target_page)
        self.update_navigation_access()
        target_page.setGraphicsEffect(None)
        self.is_animating = False

    def closeEvent(self, event):
        event.accept()
