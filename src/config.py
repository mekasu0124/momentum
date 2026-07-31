from pathlib import Path


class Config:
    APP_DIR = Path.home() / ".meks-apps/momentum"
    PROJECT_DIR = Path(__file__).parent.parent
    ICON_PATH = Path(__file__).parent / "assets/app-icon.png"