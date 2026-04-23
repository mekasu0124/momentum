from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QLabel,
    QPushButton
)

from PySide6.QtCore import Qt
from qfluentwidgets import FluentIcon as fi


class HistoryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.color_theme = parent.color_theme
        self.parent = parent

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        title = QLabel("Current Tasks")
        title.setObjectName("widget-title")
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(title)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        
        self.scroll_container = QWidget()
        self.scroll_layout = QVBoxLayout(
            self.scroll_container
        )
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.scroll_container)

        layout.addWidget(self.scroll_area, 2)

    def apply_styles(self):
        self.setStyleSheet(
            f"""
                QWidget {{
                    border: none;
                    background-color: transparent;
                }}

                QLabel#widget-title {{
                    font-style: italic;
                    font-size: 14px;
                    color: {self.color_theme['text_muted']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    border: none;
                    background-color: transparent;
                    padding-bottom: 10px;
                }}

                QLabel#no-task-label {{
                    font-style: italic;
                    font-size: 14px;
                    color: {self.color_theme['text_muted']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    border: none;
                    background-color: transparent;
                }}

                QScrollArea {{
                    border: none;
                    background-color: transparent;
                }}

                QWidget#task-card {{
                    background-color: {self.color_theme.get('surface', 'rgba(255, 255, 255, 0.05)')};
                    border-radius: {self.color_theme['border_radius_medium']};
                    margin: 0px 5px;
                }}

                QLabel#task-content {{
                    font-size: 12px;
                    color: {self.color_theme['text_primary']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    background-color: transparent;
                    padding: 10px;
                }}

                QPushButton#delete-btn {{
                    border: none;
                    border-radius: {self.color_theme['border_radius_small']};
                    background-color: transparent;
                    padding: 5px;
                    min-width: 20px;
                    max-width: 20px;
                    min-height: 20px;
                    max-height: 20px;
                }}

                QPushButton#delete-btn:hover {{
                    background-color: {self.color_theme['surface_glass_hover']};
                }}

                QPushButton#delete-btn:pressed {{
                    background-color: {self.color_theme['surface_glass']};
                }}
            """
        )

    def populate_tasks(self, tasks):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()

            if widget:
                widget.deleteLater()

        if not tasks or len(tasks) == 0:
            label = QLabel("No Tasks Exist")
            label.setObjectName("no-task-label")
            label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.scroll_layout.addWidget(label)
            self.scroll_layout.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
        
        else:
            for task in tasks:
                task_card = QWidget()
                task_card.setObjectName("task-card")
                
                task_layout = QVBoxLayout(task_card)
                task_layout.setContentsMargins(15, 10, 15, 10)
                task_layout.setSpacing(8)
                
                content_label = QLabel(task.content)
                content_label.setObjectName("task-content")
                content_label.setWordWrap(True)
                content_label.setAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )
                
                btn_row = QWidget()
                btn_layout = QHBoxLayout(btn_row)
                btn_layout.setContentsMargins(0, 0, 0, 0)
                btn_layout.setSpacing(0)
                btn_layout.addStretch()
                
                del_btn = QPushButton()
                del_btn.setObjectName("delete-btn")
                del_btn.setIcon(fi.DELETE.icon(color=self.color_theme['text_muted']))
                del_btn.setToolTip("Delete Task")
                del_btn.clicked.connect(
                    lambda checked, tid=task.id: self.parent.delete_task(tid)
                )
                
                btn_layout.addWidget(del_btn)
                
                task_layout.addWidget(content_label)
                task_layout.addWidget(btn_row)
                
                self.scroll_layout.addWidget(task_card)

            self.scroll_layout.setAlignment(
                Qt.AlignmentFlag.AlignTop
            )