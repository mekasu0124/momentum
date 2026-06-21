from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
from uuid import uuid4, UUID
from datetime import datetime

import json


class TaskRepository:
    def __init__(self, app_dir):
        self.app_dir = app_dir
        self.storage_file = Path(f"{self.app_dir}/tasks.json")

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        if not self.storage_file.exists():
            return []
        
        try:
            with open(self.storage_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            return [
                {
                    "id": task.get("id"),
                    "task": task.get("task"),
                    "created_at": task.get("created_at"),
                    "updated_at": task.get("updated_at", "")
                }
                for task in data
            ]

        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return []

        except Exception as e:
            print(f"Unknown Exception Querying Tasks:\n{e}")
            return []

    def get_task_by_id(self, task_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            task_id_uuid = UUID(task_id)
        except ValueError:
            return None, "Invalid Task UUID Format/Type"

        if not self.storage_file.exists():
            return None, f"No Task Found By ID: {task_id}"

        try:
            with open(self.storage_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            for task in data:
                if str(task.get("id")) == str(task_id_uuid):
                    return task, None

            return None, f"No Task Found By ID: {task_id}"

        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return None, "Failed to read storage file"

        except Exception as e:
            print(f"Unknown Exception Querying Task By ID:\n{e}")
            return None, "Internal error"

    def add_task(self, task: str) -> Tuple[Optional[Dict[str, Any]], str]:
        if not task or not task.strip():
            return None, "Task Cannot Be Empty"

        all_tasks = self.get_all_tasks()

        for t in all_tasks:
            if t.get("task", "").strip().lower() == task.strip().lower():
                return None, "Task Already Exists"

        new_task = {
            "id": str(uuid4()),
            "task": task.strip(),
            "created_at": datetime.now().strftime("%m/%d/%Y-%H:%M:%S"),
            "updated_at": None
        }


        all_tasks.append(new_task)

        try:
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.storage_file, 'w+', encoding="utf-8-sig") as f:
                json.dump(all_tasks, f, indent=2)

            return new_task, "Task Saved Successfully"

        except Exception as e:
            print(f"Unknown Exception Saving New Task:\n{e}")
            return None, "Failed to Save Task"

    def delete_task(self, task_id: str) -> Tuple[bool, str]:
        try:
            task_id_uuid = UUID(task_id)
        except ValueError:
            return False, "Invalid Task UUID Format/Type"

        if not self.storage_file.exists():
            return False, f"No Task Found By ID: {task_id}"

        try:
            with open(self.storage_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            original_len = len(data)
            data = [t for t in data if str(t.get("id")) != str(task_id_uuid)]

            if len(data) == original_len:
                return False, f"No Task Found By ID: {task_id}"

            with open(self.storage_file, 'w+', encoding="utf-8-sig") as f:
                json.dump(data, f, indent=2)

            return True, "Task Deleted Successfully"

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error Accessing Tasks File:\n{e}")
            return False, "Failed to Delete Task"

        except Exception as e:
            print(f"Unknown Exception Deleting Task:\n{e}")
            return False, "Failed to Delete Task"
