from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QStatusBar,
    QScrollArea,
    QLineEdit,
    QTextEdit
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextOption
from qfluentwidgets import FluentIcon as fi


class Tasks(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Tasks')

        self.logic = parent.logic
        self.color_theme = parent.color_theme
        self.async_helper = parent.async_helper

        self.status_bar = QStatusBar()

        self.target_id = None
        self.is_editing = False
        self.task_data = {
            "title": "",
            "content": ""
        }

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title = QLabel("My Tasks")
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(title)

        body_container = QWidget()
        body_layout = QHBoxLayout(body_container)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(30)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("task-list")
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()

        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setSpacing(10)

        scroll_area.setWidget(scroll_widget)
        body_layout.addWidget(scroll_area, 1)

        task_form = QWidget()
        task_layout = QVBoxLayout(task_form)
        task_layout.setContentsMargins(0, 0, 0, 0)
        task_layout.setSpacing(20)

        row1 = QWidget()
        row1_layout = QVBoxLayout(row1)
        row1_layout.setContentsMargins(0, 0, 0, 0)
        row1_layout.setSpacing(0)

        task_title = QLabel("Title")
        task_title.setObjectName("form-label")
        task_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        row1_layout.addWidget(task_title)

        self.task_title = QLineEdit()
        self.task_title.setObjectName("form-input")
        self.task_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.task_title.textChanged.connect(self.update_title_state)

        row1_layout.addWidget(self.task_title)

        task_layout.addWidget(row1)

        row2 = QWidget()
        row2_layout = QVBoxLayout(row2)
        row2_layout.setContentsMargins(0, 0, 0, 0)
        row2_layout.setSpacing(0)

        task_content = QLabel("Content")
        task_content.setObjectName("form-label")
        task_content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        row2_layout.addWidget(task_content)

        self.task_content = QTextEdit()
        self.task_content.setObjectName("form-input")
        self.task_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.task_content.textChanged.connect(self.update_content_state)

        row2_layout.addWidget(self.task_content, 2)

        task_layout.addWidget(row2, 2)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setObjectName("form-btn")
        self.submit_btn.clicked.connect(self.handle_submit)
        self.submit_btn.setFixedHeight(30)

        task_layout.addWidget(self.submit_btn)
        body_layout.addWidget(task_form, 1)

        layout.addWidget(body_container, 2)
        layout.addWidget(self.status_bar)

    def handle_error_success(self, msg: str, is_error: bool = None):
        if is_error is None:
            background = self.color_theme['warning']
            border = "orange"
            delay = 3000

        elif is_error is True:
            background = self.color_theme['error']
            border = "red"
            delay = 5000

        else:
            background = self.color_theme['success']
            border = "green"
            delay = 4000

        self.status_bar.setStyleSheet(
            f"""
                QStatusBar {{
                    background-color: {background};
                    border: 2px solid {border};
                    color: black;
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

    def showEvent(self, event):
        super().showEvent(event)

        self.handle_error_success("loading tasks", None)

        QTimer.singleShot(1500, self.load_tasks)

    def load_tasks(self):
        worker = self.async_helper.run_async(
            self.logic.task_crud.get_all_tasks
        )

        worker.signals.finished.connect(self.handle_success)
        worker.signals.error.connect(self.handle_error)

    def handle_error(self, result):
        return self.handle_error_success(result, True)

    def handle_success(self, result):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()

            if widget:
                widget.deleteLater()

        if len(result) == 0:
            label = QLabel("No Tasks Currently Exist")
            label.setObjectName("form-label")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.scroll_layout.addWidget(label)
            self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            return self.handle_error_success("tasks loaded", False)

        for task in result:
            card = QWidget()
            card.setObjectName("task-card")
            card.setFixedHeight(150)

            card_layout = QGridLayout(card)
            card_layout.setContentsMargins(10, 10, 10, 10)
            card_layout.setSpacing(5)

            card_title = QLabel(task.title)
            card_title.setObjectName("card-title")
            card_title.setAlignment(
                Qt.AlignmentFlag.AlignLeft
            )
            card_title.setScaledContents(True)

            created_at = QLabel(task.created_at)
            created_at.setObjectName("card-details")
            created_at.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            edit_btn = QPushButton(
                parent = None,
                text = "",
                icon = fi.EDIT.icon(color="#F2C94C")
            )
            edit_btn.setObjectName("task-btn")
            edit_btn.setFixedSize(70, 30)
            edit_btn.clicked.connect(
                lambda checked=False, t=task: self.edit_task(t)
            )

            del_btn = QPushButton(
                parent = None,
                text = "",
                icon = fi.DELETE.icon(color="#E85D5D")
            )
            del_btn.setObjectName("task-btn")
            del_btn.setFixedSize(70, 30)
            del_btn.clicked.connect(
                lambda checked=False, t=task: self.delete_task(t)
            )

            content_text = QTextEdit()
            content_text.setObjectName("card-content")
            content_text.setPlainText(task.content)
            content_text.setWordWrapMode(
                QTextOption.WrapMode.WordWrap
            )
            content_text.setReadOnly(True)
            content_text.setMaximumHeight(150)
            content_text.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAsNeeded
            )

            card_layout.addWidget(card_title, 0, 0, 1, 1)
            card_layout.addWidget(created_at, 0, 1, 1, 1)
            card_layout.addWidget(edit_btn, 0, 2, 1, 1)
            card_layout.addWidget(del_btn, 0, 3, 1, 1)
            card_layout.addWidget(content_text, 1, 0, 1, 4)

            card_layout.setColumnStretch(0, 3)
            card_layout.setColumnStretch(1, 1)
            card_layout.setColumnStretch(2, 0)
            card_layout.setColumnStretch(3, 0)

            card_layout.setRowStretch(0, 0)
            card_layout.setRowStretch(1, 1)

            self.scroll_layout.addWidget(card)

        self.scroll_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.handle_error_success("tasks loaded successfully", False)

    def update_title_state(self, value):
        self.task_data["title"] = value

    def update_content_state(self):
        self.task_data["content"] = self.task_content.toPlainText()

    def handle_submit(self):
        if self.is_editing:
            pass
        else:
            worker = self.async_helper.run_async(
                self.logic.task_crud.create_task,
                self.task_data
            )

            worker.signals.started.connect(
                lambda: self.handle_error_success("saving task", None)
            )
            worker.signals.finished.connect(self.task_save_success)
            worker.signals.error.connect(self.task_save_error)

    def task_save_success(self, response):
        did_save, response = response

        if did_save:
            return self.handle_error_success(response, did_save)

        self.handle_error_success(response, did_save)
        QTimer.singleShot(1500, self.load_tasks)

    def task_save_error(self, error):
        _, error = error
        self.handle_error_success(error, True)

    def edit_task(self, task):
        pass

    def delete_task(self, task):
        worker = self.async_helper.run_async(
            self.logic.task_crud.delete_task,
            task.id
        )

        worker.signals.started.connect(
            lambda: self.handle_error_success("deleting task", None)
        )
        worker.signals.finished.connect(self.task_deleted)
        worker.signals.error.connect(self.task_delete_error)

    def task_deleted(self, results):
        request, response = results

        if request:
            return self.handle_error_success(response, request)

        self.handle_error_success(response, request)
        QTimer.singleShot(1500, self.load_tasks)

    def task_delete_error(self, results):
        request, response = results

        return self.handle_error_success(response, request)