from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar,
    QScrollArea,
    QCheckBox,
    QFrame
)
from PySide6.QtCore import Qt, Signal, QTimer


class UA(QWidget):
    prev_page_signal = Signal()
    next_page_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('UA')

        self.logic = parent.logic
        self.async_helper = parent.async_helper
        self.color_theme = parent.color_theme

        self.status_bar = QStatusBar()

        self.ua_text: str = None

        self.agreements = {
            "user_agree": 0
        }

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

        title = QLabel("User Agreement")
        title.setObjectName("welcome-title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_layout.addWidget(title, 1)
        layout.addWidget(title_container)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("ua-scroll")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll_widget.setObjectName("scroll-widget")
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setSpacing(0)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area, 1)

        agreement_container = QWidget()
        agreement_container.setObjectName("agreement-container")
        agreement_layout = QVBoxLayout(agreement_container)
        agreement_layout.setContentsMargins(15, 15, 15, 15)
        agreement_layout.setSpacing(10)

        row1 = QWidget()
        row1.setObjectName("agreement-row")
        row1_layout = QHBoxLayout(row1)
        row1_layout.setContentsMargins(15, 12, 15, 12)
        row1_layout.setSpacing(20)

        agree_label = QLabel(
            "By continuing, you agree to the terms outlined in the "
            "User Agreement above. This agreement covers your rights "
            "and responsibilities when using Momentum, including data "
            "ownership, local-first architecture, and our commitment "
            "to your privacy. Do you agree to these terms?"
        )
        agree_label.setObjectName("agreement-label")
        agree_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        agree_label.setWordWrap(True)

        row1_layout.addWidget(agree_label, 1)

        user_checkbox = QCheckBox()
        user_checkbox.setObjectName("user-checkbox")
        user_checkbox.setChecked(False)
        user_checkbox.stateChanged.connect(self.update_user_agreement)
        user_checkbox.setFixedSize(20, 20)

        row1_layout.addWidget(user_checkbox)

        agreement_layout.addWidget(row1)

        layout.addWidget(agreement_container)

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

    def showEvent(self, event):
        super().showEvent(event)

        self.handle_error_success(
            "loading user agreement text... please wait...")

        self.start_ua_worker()

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

    def start_ua_worker(self) -> None:
        worker = self.async_helper.run_async(
            self.logic.get_ua_text
        )

        worker.signals.finished.connect(self.handle_ua_text_success)
        worker.signals.error.connect(self.handle_ua_text_error)

    def handle_ua_text_success(self, result):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()

            if widget:
                widget.deleteLater()

        ua_text = QLabel()
        ua_text.setObjectName("ua-text")
        ua_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ua_text.setText(result)
        ua_text.setWordWrap(True)
        ua_text.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse)

        self.scroll_layout.addWidget(ua_text)

        self.handle_error_success("loaded user agreement text", False)

    def handle_ua_text_error(self, error):
        self.handle_error_success(error, True)

    def apply_style(self):
        self.setStyleSheet(
            f"""
                QWidget#UA {{
                    background-color: {self.color_theme['background']};
                }}

                QWidget#title-container, QWidget#btn-container {{
                    background-color: transparent;
                }}

                QWidget#scroll-widget {{
                    background-color: {self.color_theme['surface']};
                    border-radius: 12px;
                }}

                QScrollArea#ua-scroll {{
                    background-color: transparent;
                    border: none;
                }}

                QScrollBar:vertical {{
                    background: {self.color_theme['surface']};
                    width: 10px;
                    border-radius: 5px;
                }}

                QScrollBar::handle:vertical {{
                    background: {self.color_theme['primary_dim']};
                    border-radius: 5px;
                    min-height: 20px;
                }}

                QScrollBar::handle:vertical:hover {{
                    background: {self.color_theme['primary']};
                }}

                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}

                QLabel#ua-text {{
                    color: {self.color_theme['text_secondary']};
                    font-size: 14px;
                    line-height: 1.8;
                    padding: 10px;
                }}

                QWidget#agreement-container {{
                    background-color: {self.color_theme['surface']};
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
                }}

                QCheckBox#user-checkbox {{
                    spacing: 5px;
                    width: 20px;
                    height: 20px;
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

    def update_user_agreement(self, state):
        self.agreements["user_agree"] = 1 if state == 2 else 0

    def handle_submit(self):
        user_value = self.agreements["user_agree"]

        self.handle_error_success(
            "updating user agreement... please wait...", None)

        if not user_value == 1:
            return self.handle_error_success("you must agree to the user agreement to use this app", True)

        worker = self.async_helper.run_async(
            self.logic.config_logic.update_user_agreement,
            self.agreements
        )

        worker.signals.finished.connect(self.handle_update_result)
        worker.signals.error.connect(self.handle_update_error)

    def handle_update_result(self, result):
        if not result:
            return self.handle_error_success("Failed to Update User Agreement", True)

        self.handle_error_success("Successfully Updated User Agreement", False)

        QTimer.singleShot(3000, lambda: self.next_page_signal.emit())

    def handle_update_error(self, error):
        self.handle_error_success("Failed to Update User Agreement", True)
