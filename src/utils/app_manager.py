from PySide6.QtGui import QPixmap


from ..new_user.app import NewUser
from ..login.app import LoginWindow
from ..app.app import Momentum


class ApplicationManager:
    def __init__(self, app, icon_path, logic, async_helper, color_theme):
        self.app = app
        self.icon_path = icon_path
        self.logic = logic
        self.async_helper = async_helper
        self.color_theme = color_theme
        self.current_window = None

    def show_main(self):
        """Show the main application window"""
        if self.current_window:
            self.current_window.close()

        window = Momentum(self.logic, self.async_helper, self.color_theme)
        window.setWindowTitle("Momentum")
        window.setWindowIcon(QPixmap(self.icon_path))
        window.setMinimumWidth(1000)
        window.setMinimumHeight(750)
        window.show()
        self.current_window = window

    def show_login(self):
        """Show the login window"""
        if self.current_window:
            self.current_window.close()

        window = LoginWindow(self.logic, self.async_helper, self.color_theme)
        window.setWindowTitle("Momentum - Login")
        window.setWindowIcon(QPixmap(self.icon_path))
        window.setMinimumWidth(1000)
        window.setMinimumHeight(750)

        # Connect signals
        window.new_user_requested.connect(self.show_new_user)
        window.login_success.connect(self.show_main)

        window.show()
        self.current_window = window

    def show_new_user(self):
        """Show the new user registration window"""
        if self.current_window:
            self.current_window.close()

        window = NewUser(self.logic, self.async_helper, self.color_theme)
        window.setWindowTitle("Momentum - New User")
        window.setWindowIcon(QPixmap(self.icon_path))
        window.setMinimumWidth(1000)
        window.setMinimumHeight(750)

        # Connect signals
        window.login_requested.connect(self.show_login)
        window.registration_success.connect(self.show_main)

        window.show()
        self.current_window = window
