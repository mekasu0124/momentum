from typing import List, Dict, Any, Tuple
from uuid import UUID

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskResponse


class TaskCrud:
    def __init__(self, parent):
        self.parent = parent

    def get_all_tasks(self) -> List[TaskResponse]:
        db = self.parent.get_db_connection()

        try:
            all_tasks = db.query(Task).all()

            return [
                TaskResponse(
                    id = str(task.id),
                    title = task.title,
                    content = task.content,
                    created_at = task.created_at.__format__("%m/%d/%Y - %H:%M:%S")
                )
                for task in all_tasks
            ]

        except Exception as e:
            print(f"Unknown Exception Querying All Tasks:\n{e}")
            self.parent.close_db_connection()
            return []

    """
    add validation to prevent hacking, or other unwanted submissions
    """
    def create_task(self, new_task: TaskCreate) -> Tuple[bool, str]:
        if not new_task:
            return True, "Task Data Cannot Be Empty"

        title = new_task.get("title", None)

        if not title:
            return True, "Title Is Required"

        content = new_task.get("content", None)

        if not content:
            return True, "Content Is Required"

        db = self.parent.get_db_connection()

        try:
            found_title = (
                db
                .query(Task)
                .filter(Task.title == title)
                .first()
            )

            if found_title:
                return True, "Title Already Exists"

            new_task = Task(
                title = title,
                content = content
            )

            db.add(new_task)
            db.commit()
            return False, "Task Saved Successfully"

        except Exception as e:
            print(F"Unknown Exception Saving New Task:\n{e}")
            self.parent.close_db_connection()
            return True, str(e)

    def delete_task(self, task_id: str) -> bool:
        if not task_id or task_id.strip() == "":
            return True, "Task ID Cannot Be Empty"

        try:
            task_uuid = UUID(task_id)

        except ValueError:
            return True, "Invalid Task ID Format"

        db = self.parent.get_db_connection()

        try:
            found_task = (
                db
                .query(Task)
                .filter(Task.id == task_uuid)
                .first()
            )

            if not found_task:
                return True, f"No Task Found By ID: {task_id[:9]}..."

            db.delete(found_task)
            db.commit()
            return False, "Task Deleted Successfully"

        except Exception as e:
            print(f"Unknown Exception Deleting Task:\n{e}")
            self.parent.close_db_connection()
            return True, str(e)