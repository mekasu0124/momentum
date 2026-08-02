from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar,
    QCheckBox
)
from PySide6.QtCore import Qt, Signal, QTimer


class Agreements(QWidget):
    prev_page_signal = Signal()
    next_page_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Agreements')

        self.logic = parent.logic
        self.async_helper = parent.async_helper
        self.color_theme = parent.color_theme

        self.status_bar = QStatusBar()

        self.tos_text: str = None

        self.agreements = {
            "read_write": 0,
            "browser": 0,
            "tos": 0,
            "ua": 0
        }

        self.setup_ui()
        self.apply_style()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        title = QLabel("Terms of Service")
        title.setObjectName("welcome-title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(title, 1)

        body_container = QWidget()
        body_container.setObjectName("agreement-container")
        
        body_layout = QVBoxLayout(body_container)
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(40)

        row1 = QWidget()
        row1.setObjectName("agreement-row")

        row1_layout = QHBoxLayout(row1)
        row1_layout.setContentsMargins(15, 12, 15, 12)
        row1_layout.setSpacing(20)

        agree_label = QLabel(
            "This application requires read/write permissions "
            "in order to create and maintain its own database "
            "and config files. All files/folders this application "
            "needs/uses to run on/with are all located in /home/"
            "<user>/.meks-apps/momentum. Do you agree to this "
            "permission? This application cannot run without it"
        )
        agree_label.setObjectName("agreement-label")
        agree_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        agree_label.setWordWrap(True)

        row1_layout.addWidget(agree_label, 1)

        rw_checkbox = QCheckBox()
        rw_checkbox.setObjectName("rw-checkbox")
        rw_checkbox.setChecked(False)
        rw_checkbox.stateChanged.connect(self.update_rw_agreement)
        rw_checkbox.setFixedSize(20, 20)

        row1_layout.addWidget(rw_checkbox)
        body_layout.addWidget(row1)

        row2 = QWidget()
        row2.setObjectName("agreement-row")

        row2_layout = QHBoxLayout(row2)
        row2_layout.setContentsMargins(15, 12, 15, 12)
        row2_layout.setSpacing(20)

        browser_label = QLabel(
            "This application requests permission to use your "
            "browser in the event you need support, or want "
            "to read more about the application without having "
            "to manually search for it on the web. This permission "
            "is completely optional. If you do not agree, this app "
            "will not use your browser whatsoever (outside of displaying "
            "static html files in your browser for the Terms of Service and "
            "user agreement information). Do you agree?"
        )
        browser_label.setObjectName("agreement-label")
        browser_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        browser_label.setWordWrap(True)

        row2_layout.addWidget(browser_label, 1)

        browser_checkbox = QCheckBox()
        browser_checkbox.setObjectName("browser-checkbox")
        browser_checkbox.setChecked(False)
        browser_checkbox.stateChanged.connect(self.update_browser_agreement)
        browser_checkbox.setFixedSize(20, 20)

        row2_layout.addWidget(browser_checkbox)
        body_layout.addWidget(row2)

        row3 = QWidget()
        row3.setObjectName("agreement-row")

        row3_layout = QHBoxLayout(row3)
        row3_layout.setContentsMargins(15, 12, 15, 12)
        row3_layout.setSpacing(20)

        tos_label = QLabel(
            "Please Read & Agree to the "
            "<a href='file:///tos.html'>Terms of Service</a>"
        )
        tos_label.setObjectName("agreement-label")
        tos_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        tos_label.setWordWrap(True)
        tos_label.setOpenExternalLinks(True)

        row3_layout.addWidget(tos_label)

        tos_checkbox = QCheckBox()
        tos_checkbox.setObjectName("tos-checkbox")
        tos_checkbox.setChecked(False)
        tos_checkbox.stateChanged.connect(self.update_tos_agreement)
        tos_checkbox.setFixedSize(20, 20)

        row3_layout.addWidget(tos_checkbox)
        body_layout.addWidget(row3)

        row4 = QWidget()
        row4.setObjectName("agreement-row")

        row4_layout = QHBoxLayout(row4)
        row4_layout.setContentsMargins(15, 12, 15, 12)
        row4_layout.setSpacing(20)

        ua_label = QLabel(
            "Please Read & Agree to the "
            "<a href='file://ua.html'>User Agreement</a>"
        )
        ua_label.setObjectName("agreement-label")
        ua_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ua_label.setWordWrap(True)
        ua_label.setOpenExternalLinks(True)

        row4_layout.addWidget(ua_label)

        ua_checkbox = QCheckBox()
        ua_checkbox.setObjectName("ua-checkbox")
        ua_checkbox.setChecked(False)
        ua_checkbox.stateChanged.connect(self.update_ua_agreement)
        ua_checkbox.setFixedSize(20, 20)

        row4_layout.addWidget(ua_checkbox)
        body_layout.addWidget(row4)
        layout.addWidget(body_container, 2)

        btn_container = QWidget()
        btn_container.setObjectName("btn-container")
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 10, 0, 0)
        btn_layout.setSpacing(20)

        btn_layout.addStretch()

        back_button = QPushButton("Back")
        back_button.setObjectName("back-btn")
        back_button.setFixedSize(160, 35)
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.clicked.connect(lambda: self.prev_page_signal.emit())

        btn_layout.addWidget(back_button)

        next_btn = QPushButton("Continue →")
        next_btn.setObjectName("next-btn")
        next_btn.setFixedSize(160, 35)
        next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        next_btn.clicked.connect(self.handle_submit)

        btn_layout.addWidget(next_btn)
        btn_layout.addStretch()

        layout.addWidget(btn_container)
        layout.addWidget(self.status_bar)

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

    def apply_style(self):
        self.setStyleSheet(
            f"""
                QWidget#TOS {{
                    background-color: {self.color_theme['background']};
                }}

                QWidget#title-container, QWidget#btn-container {{
                    background-color: transparent;
                }}

                QWidget#agreement-container {{
                    background-color: {self.color_theme['surface_elevated']};
                    border-radius: 12px;
                }}

                QWidget#agreement-row {{
                    background-color: {self.color_theme['surface_elevated']};
                    border-radius: 8px;
                }}

                QLabel#agreement-label {{
                    color: {self.color_theme['text_secondary']};
                    font-size: 13px;
                    line-height: 1.6;
                    background-color: transparent;
                }}

                QCheckBox {{
                    spacing: 5px;
                    width: 20px;
                    height: 20px;
                    background-color: white;
                }}

                QCheckBox::indicator {{
                    width: 20px;
                    height: 20px;
                    border: 2px solid {self.color_theme['border']};
                    border-radius: 4px;
                    background-color: {self.color_theme['background']};
                }}

                QCheckBox::indicator:checked {{
                    background-color: {self.color_theme['accent']};
                    border-color: {self.color_theme['accent']};
                }}

                QCheckBox::indicator:hover {{
                    border-color: {self.color_theme['accent_hover']};
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

                QPushButton#next-btn:disabled {{
                    background-color: {self.color_theme['primary_dim']};
                    border-color: {self.color_theme['primary_dim']};
                    color: {self.color_theme['text_muted']};
                }}
            """
        )

    def update_rw_agreement(self, state):
        self.agreements["read_write"] = 1 if state == 2 else 0

    def update_browser_agreement(self, state):
        self.agreements["browser"] = 1 if state == 2 else 0

    def update_tos_agreement(self, state):
        self.agreements["tos"] = 1 if state == 2 else 0

    def update_ua_agreement(self, state):
        self.agreements["ua"] = 1 if state == 2 else 0

    def handle_submit(self):
        rw_value = self.agreements["read_write"]
        tos_value = self.agreements["tos"]
        ua_value = self.agreements["ua"]

        self.handle_error_success("updating Permissions... please wait...", None)

        if not all([rw_value == 1, tos_value == 1, ua_value == 1]):
            return self.handle_error_success("You Must Agree To The Read/Write, ToS, and UA Agreements", True)

        worker = self.async_helper.run_async(
            self.logic.config_logic.update_agreements,
            self.agreements
        )

        worker.signals.finished.connect(self.handle_update_result)
        worker.signals.error.connect(self.handle_update_error)

    def handle_update_result(self, result):
        if not result:
            return self.handle_error_success("Failed to Update Agreements", True)

        self.handle_error_success("Successfully Updated Agreements", False)

        QTimer.singleShot(1500, lambda: self.next_page_signal.emit())

    def handle_update_error(self, error):
        self.handle_error_success(f"Failed to Update Agreements: {error}", True)
