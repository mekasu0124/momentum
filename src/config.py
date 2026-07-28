from pathlib import Path


class Config:
    APP_DIR = Path("~/.meks-apps/momentum").expanduser()
    ICON_PATH = Path("./src/assets/icon.png").expanduser()