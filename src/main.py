from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QPixmap
from pathlib import Path
import sys

from .app.app import Momentum
from .config import Config
from .core.crud import TaskRepository
from .core.utils.async_helper import AsyncHelper
from .core.utils.color_theme import COLOR_THEME


def get_user_agreement():
    response = QMessageBox.question(
        None,
        "Momentum Read/Write Permission Request",
        (
            "Momentum needs permission to read/write to its "
            "own storage file on your system. This program is "
            "not designed to read/write to any other medium on "
            "your device outside of the storage file located in "
            "your home directory / momentum folder.\n\nDo you agree?"
        ),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.Yes
    )
    return response == QMessageBox.Yes


def display_exit_screen():
    QMessageBox.warning(
        None,
        "Momentum Read/Write Permission Request Denied",
        (
            "You denied the permission request for this application "
            "to properly run. This application will now exit. If you "
            "change your mind later, run this app again."
        )
    )


def run_main(app, app_dir):
    color_theme = COLOR_THEME
    async_helper = AsyncHelper()
    task_repo = TaskRepository(app_dir)

    window = Momentum(app_dir, color_theme, async_helper, task_repo)
    window.setWindowTitle("Momentum")
    window.setMinimumWidth(400)
    window.setMinimumHeight(500)

    icon_path = Path(__file__).parent / "assets" / "icon.png"
    
    if icon_path.exists():
        window.setWindowIcon(QPixmap(icon_path))

    window.show()
    return app.exec()


def main():
    app = QApplication(sys.argv)
    app_dir = Path.home() / ".momentum"
    config = Config(app_dir)

    user_agreed = config.check_user_agreement()

    if not user_agreed:
        did_agree = get_user_agreement()
    
        if not did_agree:
            display_exit_screen()
            sys.exit(1)
    
        did_update = config.update_user_agreement()
    
        if not did_update:
            sys.exit(1)

    exit_code = run_main(app, app_dir)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
