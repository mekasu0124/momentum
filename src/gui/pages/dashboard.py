from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar,
)
from PySide6.QtCore import Qt, QTimer


class Dashboard(QWidget):
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

        title = QLabel("Dashboard")
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(title)

        layout.addWidget(self.status_bar)