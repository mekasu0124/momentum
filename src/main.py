from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QPixmap

import sys

from .config import Config
from .core.logic import Logic
from .gui.app import Momentum


def show_disagree():
    QMessageBox.warning(
        None,
        "Momentum Read/Write Permission Denied",
        (
            "You denied the read/write permission for "
            "this application and it cannot run without it. "
            "Run this application again if you change your mind later."
        )
    )

    sys.exit(1)


def get_user_agreement() -> bool:
    response = QMessageBox.question(
        None,
        "Momentum Read/Write Permission",
        (
            "This application requires your permission to allow "
            "it to maintain your entries within its database located "
            "here on your system at /home/<user>/.meks-apps/momentum/main.db "
            "and can be viewed by an sqlite database browser.\n\nDo You Agree?"
        ),
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.Yes
    )

    return response == QMessageBox.Yes


def main():
    app = QApplication(sys.argv)

    app_dir = Config.APP_DIR
    icon_path = Config.ICON_PATH

    logic = Logic(app_dir)

    did_agree = logic.check_agreement()

    if not did_agree:
        user_agree = get_user_agreement()

        if not user_agree:
            show_disagree()

        did_update = logic.update_user_agreement()

        if not did_update:
            sys.exit(1)

    window = Momentum(logic)
    window.setWindowTitle("Momentum")
    window.setWindowIcon(QPixmap(icon_path))
    window.setMinimumWidth(1000)
    window.setMinimumHeight(750)
    window.show()

    sys.exit(app.exec())