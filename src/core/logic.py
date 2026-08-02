from pathlib import Path

from .database.db import get_engine, get_base
from .logic_parts.config import ConfigLogic
from .logic_parts.user_logic import UserLogic
from .models.task import Task
from .models.task_graveyard import TaskGraveyard
from .models.user import User


class Logic:
    def __init__(self, app_dir: Path = None, project_dir: Path = None, async_helper = None):
        if not app_dir:
            raise ValueError("Application Directory Cannot Be Empty!")

        if not project_dir:
            raise ValueError("Project Directory for Application Project Cannot Be Empty!")

        if not async_helper:
            raise ValueError("This application is 100% asynchronous and must have an async_helper (AsyncHelper)")
        
        self.app_dir = app_dir
        self.project_dir = project_dir
        self.async_helper = async_helper
        self.config_logic = ConfigLogic(self)
        self.user_logic = UserLogic(self)

    def get_tos_text(self) -> str:
        tos_path = self.project_dir / "tos.txt"

        if not tos_path.exists():
            return "Invalid TOS Path"

        try:
            with open(tos_path, 'r') as tos_file:
                tos_text = tos_file.read()

        except FileNotFoundError:
            return "TOS File Not Found"

        except PermissionError:
            return "No Permission To Read TOS File"

        except Exception as e:
            print(f'Unknown Exception Reading TOS File:\n{e}')
            return str(e)

        else:
            return tos_text

    def get_ua_text(self) -> str:
        ua_path = self.project_dir / "ua.txt"

        if not ua_path.exists():
            return "Invalid UA Path"

        try:
            with open(ua_path, 'r') as ua_file:
                ua_text = ua_file.read()

        except FileNotFoundError:
            return "UA File Not Found"

        except PermissionError:
            return "No Permission To Read UA File"

        except Exception as e:
            print(f'Unknown Exception Reading UA File:\n{e}')
            return str(e)

        else:
            return ua_text

    def init_db(self):
        get_base().metadata.create_all(bind=get_engine())