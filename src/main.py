from PySide6.QtWidgets import QApplication

import sys

from .assets.color_theme import COLOR_THEME
from .config import Config
from .core.logic import Logic
from .utils.async_helper import AsyncHelper
from .utils.app_manager import ApplicationManager


def main():
    app = QApplication(sys.argv)

    app_dir = Config.APP_DIR
    project_dir = Config.PROJECT_DIR
    icon_path = Config.ICON_PATH
    async_helper = AsyncHelper()
    color_theme = COLOR_THEME

    logic = Logic(app_dir, project_dir, async_helper)

    manager = ApplicationManager(
        app, icon_path, logic, async_helper, color_theme
    )

    current_agreement = logic.config_logic.check_user_agreement()

    if not current_agreement:
        manager.show_new_user()
    else:
        manager.show_login()

    # Start the application event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
