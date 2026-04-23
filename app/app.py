from qfluentwidgets import (
	FluentWindow,
	FluentIcon as fi,
	Theme,
	setTheme,
	setThemeColor
)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap
from pathlib import Path

from .pages.dashboard import Dashboard

from core.logic import Logic
from core.utils.color_theme import COLOR_THEME
from core.utils.async_helper import AsyncHelper

import sys

  
class ThoughtBox(FluentWindow):
	def __init__(self, logic, async_helper, color_theme):
		super().__init__()
		
		self.logic = logic
		self.async_helper = async_helper
		self.color_theme = color_theme
		
		self.dashboard = Dashboard(self)
		
		self.init_navigation()
		self.apply_styles()
		
	def init_navigation(self):
		self.addSubInterface(
			interface = self.dashboard,
			text = "Dashboard",
			icon = fi.HOME.icon(
				color = self.color_theme['text_primary']
			)
		)
		
	def apply_styles(self):
		setTheme(Theme.AUTO)
		setThemeColor(self.color_theme['primary'])
		self.setStyleSheet(f"background-color: {self.color_theme['background']};")
		
	def closeEvent(self, event):
		self.logic.close_db_session()
		event.accept()
		

def main():
	app = QApplication(sys.argv)
	
	app_dir = Path.home() / ".momentum"
	icon_path = Path(__file__).parent / "assets" / "icon.png"
	
	if not icon_path.exists():
		print("Icon path invalid")
		icon = None
	
	else:
		icon = QPixmap(icon_path)
		
	
	logic = Logic(app_dir)
	async_helper = AsyncHelper()
	
	window = ThoughtBox(logic, async_helper, COLOR_THEME)
	window.setWindowIcon(icon)
	window.setMinimumWidth(400)
	window.setMinimumHeight(600)
	window.show()
	
	sys.exit(app.exec())
	

if __name__ == '__main__':
	main()