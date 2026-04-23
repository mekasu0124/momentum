from PySide6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
	QStatusBar,
	QLineEdit,
	QPushButton
)

from PySide6.QtCore import Qt, QTimer
from qfluentwidgets import FluentIcon as fi

from ..components.history import HistoryWidget
from ..utils.status_bar import handle_error_success


class Dashboard(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setObjectName("Dashboard")
		
		self.logic = parent.logic
		self.async_helper = parent.async_helper
		self.color_theme = parent.color_theme
		
		self.status_bar = QStatusBar()

		self.history_widget = HistoryWidget(self)
		
		self.setup_ui()
		self.apply_styles()

		self.reset_timer = QTimer()
		self.reset_timer.setInterval(1500)
		self.reset_timer.setSingleShot(True)
		self.reset_timer.timeout.connect(
			self.reset_status_bar
		)
		
	def showEvent(self, event):
		super().showEvent(event)

		handle_error_success(
			self.status_bar,
			self.color_theme,
			self.reset_timer,
			None,
			"Loading Tasks... Please Wait..."
		)

		self.load_timer = QTimer()
		self.load_timer.setInterval(1000)
		self.load_timer.setSingleShot(True)
		self.load_timer.timeout.connect(self.start_worker)
		self.load_timer.start()
		
	def setup_ui(self):
		layout = QVBoxLayout(self)
		layout.setContentsMargins(10, 10, 10, 10)
		layout.setSpacing(20)
		layout.setAlignment(
			Qt.AlignmentFlag.AlignTop |
			Qt.AlignmentFlag.AlignCenter
		)
		
		title = QLabel("Dashboard")
		title.setObjectName("page-title")
		title.setAlignment(
			Qt.AlignmentFlag.AlignLeft
		)
		
		layout.addWidget(title)
		
		body_container = QWidget()
		body_layout = QVBoxLayout(body_container)
		body_layout.setContentsMargins(0, 0, 0, 0)
		body_layout.setSpacing(20)
		body_layout.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		body_layout.addWidget(self.history_widget, 1)

		input_row = QWidget()
		input_row_layout = QHBoxLayout(input_row)
		input_row_layout.setContentsMargins(0, 0, 0, 0)
		input_row_layout.setSpacing(10)
		input_row_layout.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		self.new_task_edit = QLineEdit()
		self.new_task_edit.setObjectName("form-input")
		self.new_task_edit.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)
		self.new_task_edit.returnPressed.connect(self.save_task)

		input_row_layout.addWidget(self.new_task_edit, 2)

		self.submit_btn = QPushButton(
			text = None,
			parent = None,
			icon = fi.SEND.icon(
				color = self.color_theme['text_primary']
			)
		)
		self.submit_btn.setObjectName("form-btn")
		self.submit_btn.clicked.connect(self.save_task)

		input_row_layout.addWidget(self.submit_btn)

		body_layout.addWidget(input_row)
		
		layout.addWidget(body_container, 2)
		layout.addWidget(self.status_bar)

	def apply_styles(self):
		self.setStyleSheet(
			f"""
				QWidget {{
					border: none;
					background-color: transparent;
				}}

				QLabel#page-title {{
					font-weight: bold;
					font-style: italic;
					font-size: 16px;
					color: {self.color_theme['primary']};
					letter-spacing: 0.1em;
					word-spacing: 0.1em;
				}}

				QLineEdit {{
					border-bottom: 2px solid {self.color_theme['primary']};
					border-radius: {self.color_theme['border_radius_small']};
					background-color: transparent;
					font-size: 14px;
					color: {self.color_theme['text_muted']};
					letter-spacing: 0.1em;
					word-spacing: 0.1em;
				}}

				QLineEdit:hover {{
					border-color: {self.color_theme['accent_hover']};
					color: {self.color_theme['text_primary']};
				}}

				QLineEdit:focus {{
					border-color: {self.color_theme['focus']};
					color: {self.color_theme['focus']};
				}}
			"""
		)

	def reset_status_bar(self):
		self.status_bar.setStyleSheet("")
		self.status_bar.clearMessage()
		self.reset_timer.stop()

	def start_worker(self):
		worker = self.async_helper.run_async(
			self.logic.get_all_tasks
		)

		worker.signals.finished.connect(self.populate_tasks)
		worker.signals.error.connect(self.error_task_load)

		self.load_timer.stop()

	def error_task_load(self, error):
		handle_error_success(
			self.status_bar,
			self.color_theme,
			self.reset_timer,
			True,
			str(error)
		)

	def populate_tasks(self, tasks):
		self.history_widget.populate_tasks(tasks)

		handle_error_success(
			self.status_bar,
			self.color_theme,
			self.reset_timer,
			False,
			"Tasks Loaded"
		)

	def save_task(self):
		task_content = self.new_task_edit.text().strip()

		worker = self.async_helper.run_async(
			self.logic.save_task,
			task_content
		)

		worker.signals.finished.connect(self.success)
		worker.signals.error.connect(self.error)

	def success(self, response):
		success, response = response

		handle_error_success(
			self.status_bar,
			self.color_theme,
			self.reset_timer,
			success,
			response
		)
		
		self.new_task_edit.clear()
		self.load_timer.start()

	def error(self, error):
		handle_error_success(
			self.status_bar,
			self.color_theme,
			self.reset_timer,
			True,
			str(error)
		)

	def delete_task(self, task_id):
		worker = self.async_helper.run_async(
			self.logic.delete_task,
			task_id
		)

		worker.signals.finished.connect(self.success)
		worker.signals.error.connect(self.error)