from pathlib import Path;

import json
import os

from .database.db import get_engine, get_base, get_db
from .models.task import Task
from .crud.task import TaskCrud


class Logic:
    def __init__(self, app_dir):
        self.app_dir = Path(app_dir)
        self.config_file = self.app_dir / "config.json"
        self.db = None
        self.task_crud = TaskCrud(self)

    def check_agreement(self) -> bool:
        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            return data["read_write"] == 1

        except FileNotFoundError:
            return False

        except (KeyError, json.JSONDecodeError):
            return False

        except Exception as e:
            print(f"Unknown Exception Reading Config File:\n{e}")
            return False

    def update_user_agreement(self) -> bool:
        if not self.app_dir.exists():
            self.app_dir.mkdir(parents=True, exist_ok=True)
            
        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            data["read_write"] = 1

            with open(self.config_file, 'w+', encoding="utf-8-sig") as u:
                json.dump(data, u, indent=2)

            self.init_db()
            return True

        except FileNotFoundError:
            try:
                with open(self.config_file, 'w+', encoding="utf-8-sig") as n:
                    json.dump({"read_write": 1}, n, indent=2)

                self.init_db()

                return True

            except Exception as e:
                print(f"Unknown Exception Creating Config File:\n{e}")
                return False

        except (KeyError, json.JSONDecodeError):
            if self.config_file.exists():
                print("Invalid/Corrupt Config File. Deleteing....")
                os.remove(self.config_file)

            try:
                with open(self.config_file, 'w+', encoding="utf-8-sig") as n:
                    json.dump({"read_write": 1}, n, indent=2)

                self.init_db()

                return True

            except Exception as e:
                print(f"Unknown Exception Creating Config File:\n{e}")
                return False

        except Exception as e:
            print(f"Unknown Exception Updating Config File:\n{e}")
            return False

    def init_db(self):
        get_base().metadata.create_all(bind=get_engine())

    def get_db_connection(self):
        if self.db is None:
            self.db = next(get_db())

        return self.db

    def close_db_connection(self):
        if self.db:
            self.db.close()
            self.db = None