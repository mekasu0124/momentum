from pathlib import Path

class Config:
    """Central configuration management for the application"""
    
    APP_DIR = Path.home() / ".meks-apps"
    CONFIG_DIR = APP_DIR / "momentum"
    DB_PATH = APP_DIR / "main.db"
    CONFIG_PATH = CONFIG_DIR / "config.json"
    
    # Task validation constants
    MAX_TASK_LENGTH = 200
    MIN_TASK_LENGTH = 1
    
    @classmethod
    def ensure_directories(cls) -> None:
        """
        Create necessary directories if they don't exist
        """

        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_sqlite_url(cls) -> str:
        """
        Get the SQLite database URL
        """

        return f"sqlite:///{cls.DB_PATH}"