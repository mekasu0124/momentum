from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QStatusBar,
    QScrollArea
)
from PySide6.QtCore import Qt, QTimer
from typing import Dict, Any, List


class Momentum(QMainWindow):
    # Fixed signature: accept app_dir first (though unused, keep for consistency)
    def __init__(self, app_dir, color_theme, async_helper, task_repo):
        super().__init__()

        self.app_dir = app_dir
        self.color_theme = color_theme
        self.async_helper = async_helper
        self.task_repo = task_repo
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)          # Attach status bar

        # Store task widgets for later deletion/update
        self.task_widgets = []

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Scroll area for task history
        task_history = QScrollArea()
        task_history.setWidgetResizable(True)
        task_container = QWidget()
        self.task_history_layout = QVBoxLayout(task_container)
        self.task_history_layout.setContentsMargins(0, 0, 0, 0)
        self.task_history_layout.setSpacing(
            5)      # Slight spacing between tasks
        task_history.setWidget(task_container)
        layout.addWidget(task_history)

        # Input form
        form_container = QWidget()
        form_layout = QHBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(10)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter Task Here...")
        self.task_input.returnPressed.connect(
            self.save_task)   # renamed method

        form_layout.addWidget(self.task_input)

        submit_btn = QPushButton("Save")
        submit_btn.clicked.connect(self.save_task)
        form_layout.addWidget(submit_btn)           # FIX: add button

        layout.addWidget(form_container)

    def apply_styles(self):
        # (unchanged, uses self.color_theme)
        self.setStyleSheet(
            f"""
                QMainWindow {{
                    background-color: {self.color_theme['background']};
                    border: none;
                }}
                QScrollArea {{
                    background-color: transparent;
                    border: 2px solid {self.color_theme['accent']};
                    border-radius: 8px;
                }}
                QPushButton {{
                    border: 2px solid {self.color_theme['accent']};
                    border-radius: 12px;
                    font-weight: normal;
                    font-style: normal;
                    font-size: 12px;
                    color: {self.color_theme['text_muted']};
                    letter-spacing: 0.1em;
                    outline: none;
                }}
                QPushButton:hover {{
                    border-color: {self.color_theme['accent_hover']};
                    color: {self.color_theme['text_primary']};
                    font-weight: bold;
                    font-style: italic;
                    outline: none;
                }}
                QLineEdit {{
                    background-color: transparent;
                    border: none;
                    border-bottom: 2px solid {self.color_theme['accent']};
                    font-weight: normal;
                    font-style: normal;
                    font-size: 12px;
                    color: {self.color_theme['text_muted']};
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    outline: none;
                }}
                QLineEdit:hover {{
                    background-color: {self.color_theme['surface_elevated']};
                    border-color: {self.color_theme['accent_hover']};
                    font-weight: bold;
                    font-style: italic;
                    color: {self.color_theme['text_primary']};
                    outline: none;
                }}
                QLineEdit:focus {{
                    background-color: {self.color_theme['surface_light']};
                }}
                QLabel {{
                    color: {self.color_theme['text_primary']};
                }}
                QLabel#task-complete {{
                    color: {self.color_theme['text_muted']};
                    text-decoration: line-through;
                }}
            """
        )

    # ------- Status bar helper -------
    def show_status(self, message: str, is_error: bool = False):
        self.status_bar.showMessage(message, 3000)
        if is_error:
            # Optional: change status bar color for errors
            pass

    # ------- Task Save (renamed from save_worker) -------
    def save_task(self):
        task_text = self.task_input.text().strip()
        if not task_text:
            self.show_status("Task cannot be empty", is_error=True)
            return

        worker = self.async_helper.run_async(
            self.task_repo.add_task,   # method name is add_task, not save_task
            task_text
        )
        worker.signals.finished.connect(self.on_task_saved)
        worker.signals.error.connect(self.on_task_error)
        worker.signals.started.connect(
            lambda: self.show_status("Saving task...")
        )

    # ------- Load tasks on show -------
    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(150, self.start_worker)

    def start_worker(self):
        worker = self.async_helper.run_async(self.task_repo.get_all_tasks)
        worker.signals.finished.connect(self.on_tasks_loaded)
        worker.signals.error.connect(self.on_task_error)
        worker.signals.started.connect(
            lambda: self.show_status("Loading tasks...")
        )

    # ------- UI Update Slots -------
    def on_tasks_loaded(self, tasks: List[Dict[str, Any]]):
        # Clear existing task widgets
        self.clear_task_list()
        for task in tasks:
            self.add_task_widget(task)
        self.show_status(f"Loaded {len(tasks)} tasks")

    def on_task_saved(self, result):
        # result is (new_task_dict, message) from add_task
        task, msg = result
        if task is None:
            self.show_status(f"Error: {msg}", is_error=True)
            return
        # Add new task to UI
        self.add_task_widget(task)
        self.task_input.clear()
        self.show_status(msg)

    def on_task_deleted(self, result):
        # result is (success, message) from delete_task
        success, msg = result
        if success:
            # Refresh the whole list to reflect deletion
            self.start_worker()   # reload all tasks
        else:
            self.show_status(f"Error: {msg}", is_error=True)

    def on_task_error(self, error_msg: str):
        self.show_status(f"Error: {error_msg}", is_error=True)

    # ------- UI Helpers -------
    def clear_task_list(self):
        # Remove all widgets from the task history layout
        while self.task_history_layout.count():
            item = self.task_history_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.task_widgets.clear()

    def add_task_widget(self, task: Dict[str, Any]):
        # Create a row with checkbox, label, and delete button
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(5)

        checkbox = QCheckBox()
        # We'll use checkbox state to mark as complete (visual only)
        checkbox.stateChanged.connect(
            lambda state, lbl=QLabel(
                task["task"]): self.toggle_task_complete(lbl, state)
        )
        row_layout.addWidget(checkbox)

        label = QLabel(task["task"])
        label.setWordWrap(True)
        row_layout.addWidget(label)

        delete_btn = QPushButton("×")
        delete_btn.setFixedSize(24, 24)
        delete_btn.setStyleSheet("border: none; font-size: 16px; color: red;")
        delete_btn.clicked.connect(
            lambda checked, tid=task["id"]: self.delete_task(tid)
        )
        row_layout.addWidget(delete_btn)

        self.task_history_layout.addWidget(row_widget)
        self.task_widgets.append(row_widget)

    def toggle_task_complete(self, label: QLabel, state: int):
        if state == Qt.Checked:
            label.setObjectName("task-complete")
        else:
            label.setObjectName("")   # reset
        # Reapply styles to update
        label.style().unpolish(label)
        label.style().polish(label)

    def delete_task(self, task_id: str):
        worker = self.async_helper.run_async(
            self.task_repo.delete_task, task_id)
        worker.signals.finished.connect(self.on_task_deleted)
        worker.signals.error.connect(self.on_task_error)
        worker.signals.started.connect(
            lambda: self.show_status("Deleting task...")
        )
