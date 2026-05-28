from pathlib import Path
from typing import Tuple, Union, List, Dict, Any
from uuid import UUID, uuid4

import tomllib
import json
import sys
import os

from .database.db import get_base, get_engine, get_db
from .models.task import Task


class Logic:
    def __init__(self, app_dir):
        self.app_dir = app_dir
        self.config_file = Path(f"{self.app_dir}/momentum/config.json")
        self.init_environment()

    def init_environment(self):
        if not self.config_file.exists():
            self.get_user_agreement()

        else:
            self.check_user_agreement()

    def check_user_agreement(self):
        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            if not data.get("rw_perms") == 1:
                self.get_user_agreement()

            else:
                self.init_db()

        except FileNotFoundError:
            print(f"File Not Found: '{self.config_file}'")
            self.get_user_agreement()

        except (KeyError, json.JSONDecodeError):
            print(f"Config File is Corrupt. Deleteing and re-creating... Please Wait...")

            if self.config_file.exists():
                os.remove(self.config_file)

            self.get_user_agreement()

        except Exception as e:
            print(f"Unknown Exception Reading System Config:\n{e}")
            sys.exit(1)

    def get_user_agreement(self):
        prompt = (
            "Momentum requires permissions to read/write to its "
            "own database and update its files when an update "
            "comes available. This application cannot run without "
            "these permissions.\n\nDo you agree to allow this application "
            "to have read/write permissions to its own database file and code "
            "base?\n\nDo You Agree? (Y/N): "
        )
        valid_options = ['Y', 'N', 'y', 'n']

        user_agree = input(prompt)

        while not user_agree in valid_options:
            print("\nInvalid Input. 'Y' for Yes or 'N' for No\n\n")

            user_agree = input(prompt)

            if user_agree in valid_options:
                break

        if user_agree.lower() == 'n':
            print(
                "You denied the read/write permissions for this "
                "application. If you change your mind in the future, "
                "run this command again."
            )
            sys.exit(0)

        else:
            self.update_user_config()

    def update_user_config(self):
        momentum_dir = self.config_file.parent

        if not momentum_dir.exists():
            momentum_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            data["rw_perms"] = 1

            with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                json.dump(data, new, indent=2)

            self.init_db()

        except FileNotFoundError:
            print("config file not found. creating new config file... please wait...")
            try:
                with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                    json.dump({"rw_perms": 1}, new, indent=2)

                self.init_db()

            except Exception as e:
                print(f"Unknown Exception Creating Config File:\n{e}")
                sys.exit(1)

        except (KeyError, json.JSONDecodeError):
            print('Config File is Corrupt. Deleting and re-creating... please wait...')

            if self.config_file.exists():
                os.remove(self.config_file)

            with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                json.dump({"rw_perms": 1}, new, indent=2)

            self.init_db()

        except Exception as e:
            print(f"Unknown Exception Updating User Config:\n{e}")
            sys.exit(1)

    def init_db(self):
        get_base().metadata.create_all(
            bind=get_engine()
        )

    def get_pyproject_data(self):
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        
        with open(pyproject_path, 'rb') as project:
            proj_data = tomllib.load(project)

        if not "project" in proj_data:
            return {}

        my_dict = {
            "project": {},
            "urls": {},
            "scripts": {}
        }
        
        project_data = proj_data["project"]

        for key, value in project_data.items():
            if key == "urls":
                for k, v in project_data["urls"].items():
                    my_dict["urls"][k] = v

            if key == "scripts":
                for j, u in project_data["scripts"].items():
                    my_dict["scripts"][j] = u

            if key != "urls" and key != "scripts":
                my_dict["project"][key] = value

        return my_dict
    
    def add_task(self, new_task: str) -> str:
        db = next(get_db())

        try:
            found_task = (
                db
                .query(Task)
                .filter(Task.task == new_task)
                .first()
            )

            if found_task:
                return "Task Already Exists"
            
            task_to_save = Task(task=new_task)

            db.add(task_to_save)
            db.commit()
            return "Task Saved Successfully"
        
        except Exception as e:
            print(f"Unknown Exception Saving New Task:\n{e}")
            db.rollback()
            return "Failed to Save Task"
        
    def edit_task(self, task_id: str, updated_task: str, is_completed: bool = False) -> str:
        db = next(get_db())

        try:
            try:
                task_uuid = UUID(task_id)
            except ValueError:
                return f"Invalid UUID Format: {task_id}"
            
            found_task = (
                db
                .query(Task)
                .filter(Task.id == task_uuid)
                .first()
            )

            if not found_task:
                return f"No Task Found By ID: {task_id}"
            
            found_task.task = updated_task

            if is_completed:
                found_task.is_completed = True

            db.commit()
            db.refresh(found_task)
            return "Task Updated Successfully"
        
        except Exception as e:
            print(f"Unknown Exception Updating Task:\n{e}")
            db.rollback()
            return "Failed to Updated Task"

    def delete_task(self, task_id: UUID) -> str:
        db = next(get_db())

        try:
            try:
                task_uuid = UUID(task_id)
            except ValueError:
                return f"Invalid UUID Format: {task_id}"
            
            found_task = (
                db
                .query(Task)
                .filter(Task.id == task_uuid)
                .first()
            )

            if not found_task:
                return f"No Task Found By ID: {task_id}"
            
            db.delete(found_task)
            db.commit()
            return "Task Deleted Successfully"
        
        except Exception as e:
            print(f'Unknown Exception Deleting Task:\n{e}')
            db.rollback()
            return "Failed to Delete Task"

    def list_tasks(self) -> Dict[str, Any]:
        db = next(get_db())

        try:
            return db.query(Task).all()
        
        except Exception as e:
            print(f"Unknown Exception Querying All Tasks:\n{e}")
            db.rollback()
            return []

    def list_task_by_id(self, task_id: str) -> Union[Dict[str, str], None]:
        db = next(get_db())

        try:
            try:
                task_uuid = UUID(task_id)
            except ValueError:
                return f"Invalid UUID Format: {task_id}"
            
            found_task = (
                db
                .query(Task)
                .filter(Task.id == task_uuid)
                .first()
            )

            return found_task
        
        except Exception as e:
            print(f"Unknown Exception Querying Single Task:\n{e}")
            db.rollback()
            return None