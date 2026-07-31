from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar
)
from PySide6.QtCore import Qt, Signal


class Dashboard(QWidget):
    launch_user_registration = Signal()
    login_success = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Dashboard')

        self.logic = parent.logic
        self.color_theme = parent.color_theme

        self.status_bar = QStatusBar()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        title = QLabel("Welcome to Momentum!")
        title.setObjectName("welcome-title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_layout.addWidget(title, 1)

        register_button = QPushButton("New User?")
        register_button.setObjectName("register-btn")
        register_button.clicked.connect(
            lambda: self.launch_user_registration.emit()
        )

        title_layout.addWidget(register_button)

        layout.addWidget(title_container)

        # Login button for demonstration
        login_button = QPushButton("Login")
        login_button.setObjectName("login-btn")
        login_button.clicked.connect(
            lambda: self.login_success.emit()
        )
        layout.addWidget(login_button)
