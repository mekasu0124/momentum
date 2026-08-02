from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar,
    QFrame
)
from PySide6.QtCore import Qt, Signal

import sys

"""
TODO - rename welcome.py to page_one.py
TODO - move read/write and browser agreement check to page_two.py
TODO - move tos and ua file text to static html files
TODO - move toa and ua agreement to page_two.py
TODO - update logic on backend
"""


class Welcome(QWidget):
    launch_user_login = Signal()
    next_page_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Welcome')

        self.logic = parent.logic
        self.async_helper = parent.async_helper
        self.color_theme = parent.color_theme

        self.status_bar = QStatusBar()

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        title_container = QWidget()
        title_container.setObjectName("title-container")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        title = QLabel("Welcome to Momentum!")
        title.setObjectName("welcome-title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_layout.addWidget(title, 1)

        login_button = QPushButton("Already Registered?")
        login_button.setObjectName("login-btn")
        login_button.clicked.connect(
            lambda: self.launch_user_login.emit()
        )
        login_button.setCursor(Qt.CursorShape.PointingHandCursor)

        title_layout.addWidget(login_button)
        layout.addWidget(title_container)

        body_container = QWidget()
        body_container.setObjectName("body-container")
        body_layout = QVBoxLayout(body_container)
        body_layout.setContentsMargins(20, 20, 20, 20)
        body_layout.setSpacing(12)
        body_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        intro = QLabel(
            "Momentum is a feature-rich, security-first, local-storage-first task management application. "
            "All your important data stays on your device, accessible via <b>~/.meks-apps/momentum</b>."
        )
        intro.setObjectName("body-text")
        intro.setWordWrap(True)
        intro.setAlignment(Qt.AlignmentFlag.AlignJustify)

        body_layout.addWidget(intro)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setObjectName("separator")
        body_layout.addWidget(line)

        features_title = QLabel("Key Features:")
        features_title.setObjectName("features-title")
        body_layout.addWidget(features_title)

        features = [
            "• All data stored locally – no cloud dependency",
            "• Username + password security with password recovery",
            "• Full read/write permissions required for local storage",
            "• Password reset via email (temporary password sent)",
            "• Easy migration – your data stays in your home directory"
        ]
        for feature in features:
            label = QLabel(feature)
            label.setObjectName("feature-item")
            label.setWordWrap(True)
            body_layout.addWidget(label)

        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        line2.setObjectName("separator")
        body_layout.addWidget(line2)

        note = QLabel(
            "If you ever forget your password, the login screen provides a password reset option. "
            "Enter your email address, and a temporary password will be sent to you. "
            "After logging in with the temporary password, you'll be prompted to set a new one."
        )
        note.setObjectName("body-text")
        note.setWordWrap(True)
        note.setAlignment(Qt.AlignmentFlag.AlignJustify)

        body_layout.addWidget(note)
        body_layout.addStretch()

        layout.addWidget(body_container, 1)

        btn_container = QWidget()
        btn_container.setObjectName("btn-container")
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 10, 0, 0)
        btn_layout.setSpacing(20)

        btn_layout.addStretch()

        exit_btn = QPushButton("Exit Application")
        exit_btn.setObjectName("exit-btn")
        exit_btn.setFixedSize(160, 35)
        exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_btn.clicked.connect(lambda: sys.exit(0))

        btn_layout.addWidget(exit_btn)

        next_btn = QPushButton("Continue →")
        next_btn.setObjectName("next-btn")
        next_btn.setFixedSize(160, 35)
        next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        next_btn.clicked.connect(lambda: self.next_page_signal.emit())

        btn_layout.addWidget(next_btn)
        btn_layout.addStretch()

        layout.addWidget(btn_container)
        layout.addWidget(self.status_bar)

    def apply_styles(self):
        self.setStyleSheet(
            f"""
                QWidget#Welcome {{
                    background-color: {self.color_theme['background']};
                }}

                QWidget#title-container, QWidget#body-container, QWidget#btn-container {{
                    background-color: transparent;
                }}

                QPushButton#login-btn {{
                    background-color: transparent;
                    border: none;
                    font-size: 13px;
                    color: {self.color_theme['text_muted']};
                    padding: 8px 16px;
                    border-radius: 6px;
                }}

                QPushButton#login-btn:hover {{
                    background-color: {self.color_theme['surface_elevated']};
                    color: {self.color_theme['text_secondary']};
                }}

                QLabel#body-text {{
                    color: {self.color_theme['text_secondary']};
                    font-size: 15px;
                    line-height: 1.6;
                    padding: 5px 0;
                }}

                QLabel#features-title {{
                    color: {self.color_theme['accent']};
                    font-weight: bold;
                    font-size: 16px;
                    padding: 10px 0 5px 0;
                }}

                QLabel#feature-item {{
                    color: {self.color_theme['text_secondary']};
                    font-size: 14px;
                    padding: 2px 0 2px 20px;
                }}

                QFrame#separator {{
                    background-color: {self.color_theme['border']};
                    max-height: 1px;
                    margin: 10px 0;
                }}

                QPushButton#exit-btn {{
                    border: 1px solid {self.color_theme['error']};
                    border-radius: 8px;
                    background-color: transparent;
                    font-size: 14px;
                    color: {self.color_theme['text_secondary']};
                    padding: 8px 16px;
                }}

                QPushButton#exit-btn:hover {{
                    background-color: {self.color_theme['error']};
                    color: {self.color_theme['text_primary']};
                    border-color: {self.color_theme['error']};
                }}

                QPushButton#next-btn {{
                    border: 1px solid {self.color_theme['accent']};
                    border-radius: 8px;
                    background-color: {self.color_theme['accent']};
                    font-size: 14px;
                    font-weight: bold;
                    color: {self.color_theme['background']};
                    padding: 8px 16px;
                }}

                QPushButton#next-btn:hover {{
                    background-color: {self.color_theme['accent_hover']};
                    border-color: {self.color_theme['accent_hover']};
                }}
            """
        )
