from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar,
    QLineEdit
)
from PySide6.QtCore import Qt, Signal, QTimer


class Register(QWidget):
    registration_success = Signal()
    prev_page_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Register')

        self.logic = parent.logic
        self.async_helper = parent.async_helper
        self.color_theme = parent.color_theme

        self.status_bar = QStatusBar()

        self.setup_ui()
        self.apply_style()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        title_container = QWidget()
        title_container.setObjectName("title-container")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        title = QLabel("Let's Get You Setup With A New Account!")
        title.setObjectName("welcome-title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_layout.addWidget(title, 1)
        layout.addWidget(title_container)

        center_container = QWidget()
        center_container.setObjectName("center-container")
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        center_layout.addStretch()

        form_container = QWidget()
        form_container.setObjectName("form-container")
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(12)
        form_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body_container = QWidget()
        body_container.setObjectName("body-container")
        body_layout = QVBoxLayout(body_container)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(12)

        row1 = QWidget()
        row1.setObjectName("form-row")
        row1_layout = QHBoxLayout(row1)
        row1_layout.setContentsMargins(0, 0, 0, 0)
        row1_layout.setSpacing(20)

        email_label = QLabel("Email Address")
        email_label.setObjectName("form-label")
        email_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        email_label.setFixedWidth(120)

        row1_layout.addWidget(email_label)

        self.email_edit = QLineEdit()
        self.email_edit.setObjectName("form-input")
        self.email_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.email_edit.setPlaceholderText("email@example.com")
        self.email_edit.setFixedWidth(350)

        row1_layout.addWidget(self.email_edit)

        body_layout.addWidget(row1)

        row2 = QWidget()
        row2.setObjectName("form-row")
        row2_layout = QHBoxLayout(row2)
        row2_layout.setContentsMargins(0, 0, 0, 0)
        row2_layout.setSpacing(20)

        username_label = QLabel("Create Username")
        username_label.setObjectName("form-label")
        username_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        username_label.setFixedWidth(120)

        row2_layout.addWidget(username_label)

        self.username_edit = QLineEdit()
        self.username_edit.setObjectName("form-input")
        self.username_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.username_edit.setPlaceholderText("john_doe123")
        self.username_edit.setFixedWidth(350)
        self.username_edit.setToolTip(
            "Username Must Be At Least 8 Characters Long, Max 15 Characters\n"
            "and can only use letters a-z A-Z, numbers 0-9, and either an under"
            "score or hyphen.\nusernames cannot begin with a number or special"
            "character"
        )

        row2_layout.addWidget(self.username_edit)

        body_layout.addWidget(row2)

        row3 = QWidget()
        row3.setObjectName("form-row")
        row3_layout = QHBoxLayout(row3)
        row3_layout.setContentsMargins(0, 0, 0, 0)
        row3_layout.setSpacing(20)

        create_pw_label = QLabel("Create Password")
        create_pw_label.setObjectName("form-label")
        create_pw_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        create_pw_label.setFixedWidth(120)

        row3_layout.addWidget(create_pw_label)

        self.create_pw_edit = QLineEdit()
        self.create_pw_edit.setObjectName("form-input")
        self.create_pw_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.create_pw_edit.setPlaceholderText("Password123!")
        self.create_pw_edit.setEchoMode(QLineEdit.Password)
        self.create_pw_edit.setFixedWidth(350)
        self.create_pw_edit.setToolTip(
            "Password:\n"
            "  - must be at least 8 characters long\n"
            "  - cannot start with a number or special character\n"
            "  - can only use lower case a-z, uppercase A-Z\n"
            "  - can only use numbers 0-9\n"
            "  - can only use special characters: !@#$%^&*()_+-=.,"
        )

        row3_layout.addWidget(self.create_pw_edit)

        body_layout.addWidget(row3)

        row4 = QWidget()
        row4.setObjectName("form-row")
        row4_layout = QHBoxLayout(row4)
        row4_layout.setContentsMargins(0, 0, 0, 0)
        row4_layout.setSpacing(20)

        confirm_pw_label = QLabel("Confirm Password")
        confirm_pw_label.setObjectName("form-label")
        confirm_pw_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        confirm_pw_label.setFixedWidth(120)

        row4_layout.addWidget(confirm_pw_label)

        self.confirm_pw_edit = QLineEdit()
        self.confirm_pw_edit.setObjectName("form-input")
        self.confirm_pw_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.confirm_pw_edit.setPlaceholderText("Password123!")
        self.confirm_pw_edit.setEchoMode(QLineEdit.Password)
        self.confirm_pw_edit.setFixedWidth(350)
        self.confirm_pw_edit.setToolTip(
            "Password:\n"
            "  - must be at least 8 characters long\n"
            "  - cannot start with a number or special character\n"
            "  - can only use lower case a-z, uppercase A-Z\n"
            "  - can only use numbers 0-9\n"
            "  - can only use special characters: !@#$%^&*()_+-=.,"
        )

        row4_layout.addWidget(self.confirm_pw_edit)

        body_layout.addWidget(row4)

        form_layout.addWidget(body_container)

        btn_container = QWidget()
        btn_container.setObjectName("btn-container")
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 20, 0, 0)
        btn_layout.setSpacing(20)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("back-btn")
        back_btn.setFixedSize(160, 35)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.prev_page_signal.emit())

        btn_layout.addStretch()
        btn_layout.addWidget(back_btn)

        login_btn = QPushButton("Register")
        login_btn.setObjectName("login-btn")
        login_btn.setFixedSize(160, 35)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.clicked.connect(self.handle_submit)

        btn_layout.addWidget(login_btn)
        btn_layout.addStretch()

        form_layout.addWidget(btn_container)

        center_layout.addWidget(form_container)
        center_layout.addStretch()

        layout.addWidget(center_container, 1)
        layout.addWidget(self.status_bar)

    def apply_style(self):
        self.setStyleSheet(
            f"""
                QWidget#Register {{
                    background-color: {self.color_theme['background']};
                }}

                QWidget#title-container, QWidget#center-container {{
                    background-color: transparent;
                }}

                QWidget#form-container {{
                    background-color: transparent;
                }}

                QWidget#form-row {{
                    background-color: transparent;
                }}

                QLabel#form-label {{
                    color: {self.color_theme['text_secondary']};
                    font-size: 14px;
                    font-weight: bold;
                }}

                QLineEdit#form-input {{
                    background-color: {self.color_theme['surface']};
                    color: {self.color_theme['text_secondary']};
                    border: 1px solid {self.color_theme['border']};
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 14px;
                }}

                QLineEdit#form-input:focus {{
                    border: 1px solid {self.color_theme['accent']};
                }}

                QLineEdit#form-input:hover {{
                    border: 1px solid {self.color_theme['border_active']};
                }}

                QPushButton#back-btn {{
                    border: 1px solid {self.color_theme['error']};
                    border-radius: 8px;
                    background-color: transparent;
                    font-size: 14px;
                    color: {self.color_theme['text_secondary']};
                    padding: 8px 16px;
                }}

                QPushButton#back-btn:hover {{
                    background-color: {self.color_theme['error']};
                    color: {self.color_theme['text_primary']};
                    border-color: {self.color_theme['error']};
                }}

                QPushButton#login-btn {{
                    border: 1px solid {self.color_theme['success']};
                    border-radius: 8px;
                    background-color: {self.color_theme['success']};
                    font-size: 14px;
                    font-weight: bold;
                    color: {self.color_theme['background']};
                    padding: 8px 16px;
                }}

                QPushButton#login-btn:hover {{
                    background-color: #3BE68C;
                    border-color: #3BE68C;
                }}
            """
        )

    def handle_error_success(self, msg: str, is_error: bool = None):
        if is_error is None:
            background = self.color_theme['warning']
            border = "orange"
            delay = 4000

        elif is_error:
            background = self.color_theme['error']
            border = "red"
            delay = 5000

        else:
            background = self.color_theme['success']
            border = "green"
            delay = 3000

        self.status_bar.setStyleSheet(
            f"""
                QStatusBar {{
                    background-color: {background};
                    border: 2px solid {border};
                    color: black;
                    font-size: 14px;
                    font-style: italic;
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                }}
            """
        )
        self.status_bar.showMessage(msg)

        QTimer.singleShot(delay, self.reset_status_bar)

    def reset_status_bar(self):
        self.status_bar.clearMessage()
        self.status_bar.setStyleSheet("")

    def handle_submit(self):
        self.handle_error_success("Registering User... please wait...", None)

        email = self.email_edit.text().strip()
        username = self.username_edit.text().strip()
        create_pw = self.create_pw_edit.text().strip()
        confirm_pw = self.confirm_pw_edit.text().strip()

        self.user_dict = {
            "email": email,
            "username": username,
            "cr_password": create_pw,
            "cf_password": confirm_pw
        }

        worker = self.async_helper.run_async(
            self.logic.user_logic.create_user,
            self.user_dict
        )

        worker.signals.finished.connect(self.handle_create_success)
        worker.signals.error.connect(self.handle_create_error)

    def handle_create_success(self, result):
        if not result:
            return self.handle_error_success("Failed to Register New User", True)

        self.handle_error_success("Successfully Registered User", False)

        QTimer.singleShot(1500, lambda: self.registration_success.emit())

    def handle_create_error(self, error):
        self.handle_error_success(f"Failed to Register New User: {error}", True)
