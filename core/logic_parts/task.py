from typing import Tuple, List, Optional
from uuid import UUID

from ..database.db import get_db
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..validators import validate_task_name


class TaskLogic:
    def __init__(self, parent=None):
        self.logger = parent.logger

    def add_task(self, new_task: str) -> Tuple[bool, Optional[TaskResponse], Optional[str]]:
        """
        CRUD operation to add a new task to the database.
        
        Params:
            - new_task: str

        Returns:
            - Tuple[bool, Optional[TaskResponse], Optional[str]]
        """

        if not validate_task_name(new_task):
            return False, None, "Invalid Task"

        try:
            stripped_task = new_task.strip()
            task_create = TaskCreate(task=stripped_task)

        except Exception as e:
            self.logger.error(f"Validation Error:\n{e}")
            return False, None, "Invalid Task Data Format"
        
        with get_db() as db:
            try:            
                found_task = (
                    db
                    .query(Task)
                    .filter(Task.task == task_create.task)
                    .first()
                )

                if found_task:
                    return False, None, "Task Already Exists"
                
                task_to_save = Task(task=task_create.task)

                db.add(task_to_save)
                db.commit()
                db.refresh(task_to_save)

                task_response = TaskResponse(
                    id = str(task_to_save.id),
                    task = task_to_save.task,
                    is_completed = task_to_save.is_completed,
                    created_at = task_to_save.created_at
                )

                return True, task_response, "Task Saved Successfully"
            
            except Exception as e:
                self.logger.error(f"Unknown Exception Saving New Task:\n{e}")
                return False, None, "Failed to Save Task"
        
    def edit_task(
        self, 
        task_id: str, 
        updated_task: Optional[str] = None, 
        is_completed: Optional[bool] = None
    ) -> Tuple[bool, Optional[TaskResponse], str]:
        """
        CRUD operation to edit a task in the database.

        Params:
            - task_id: str - the string representations of the tasks UUID of the task to update
            - updated_task: str - the updated task information
            - is_compelted: bool - the updated status of the task. False by default

        Returns:
            - Tuple[bool, Optional[TaskResponse], Optional[str]]
        """

        if updated_task is not None and not validate_task_name(updated_task):
            return False, None, "Invalid Task"
        
        try:
            task_uuid = UUID(task_id)

        except ValueError:
            return False, None, f"Invalid UUID Format: {task_id}"
        
        if updated_task is None and is_completed is None:
            return False, None, "Nothing to Update - Provide --task or --is_complete"
        
        try:
            task_update = TaskUpdate(
                task = updated_task,
                is_completed = is_completed
            )

        except Exception as e:
            self.logger.error(f"Validation Error:\n{e}")
            return False, None, "Invalid Task Data Format"
        
        with get_db() as db:
            try:
                found_task = (
                    db
                    .query(Task)
                    .filter(Task.id == task_uuid)
                    .first()
                )

                if not found_task:
                    return False, None, f"No Task Found By ID: {task_id}"
                
                if task_update.task is not None:                    
                    duplicate_task = (
                        db
                        .query(Task)
                        .filter(
                            Task.task == task_update.task,
                            Task.id != task_uuid
                        )
                        .first()
                    )

                    if duplicate_task:
                        return False, None, f"Task Already Exists"
                    
                    found_task.task = task_update.task

                if task_update.is_completed is not None:
                    found_task.is_completed = task_update.is_completed

                db.commit()
                db.refresh(found_task)

                task_response = TaskResponse(
                    id = str(found_task.id),
                    task = found_task.task,
                    is_completed = found_task.is_completed,
                    created_at = found_task.created_at,
                    updated_at = found_task.updated_at
                )

                return True, task_response, "Task Updated Successfully"
            
            except Exception as e:
                self.logger.error(f"Unknown Exception Updating Task:\n{e}")
                return False, None, "Failed to Update Task"

    def delete_task(self, task_id: str) -> Tuple[bool, str]:
        """
        Delete a task from the database.

        Params:
            - task_id: str - the string representation of the task's UUID

        Returns:
            - Tuple[bool, str]
        """

        try:
            task_uuid = UUID(task_id)

        except ValueError:
            return False, f"Invalid UUID Format: {task_id}"

        with get_db() as db:
            try:            
                found_task = (
                    db
                    .query(Task)
                    .filter(Task.id == task_uuid)
                    .first()
                )

                if not found_task:
                    return False, f"No Task Found By ID: {task_id}"
                
                db.delete(found_task)
                db.commit()
                return True, "Task Deleted Successfully"
            
            except Exception as e:
                self.logger.error(f'Unknown Exception Deleting Task:\n{e}')
                return False, "Failed to Delete Task"

    def list_tasks(self) -> List[TaskResponse]:
        """
        List all tasks in the database

        Params:
            - None

        Returns:
            - List[TaskResponse]
        """

        with get_db() as db:
            try:
                tasks = db.query(Task).all()

                task_responses = []

                for existing_task in tasks:
                    task_responses.append(
                        TaskResponse(
                            id = str(existing_task.id),
                            task = existing_task.task,
                            is_completed = existing_task.is_completed,
                            created_at = existing_task.created_at,
                            updated_at = existing_task.updated_at
                        )
                    )

                return task_responses
            
            except Exception as e:
                self.logger.error(f"Unknown Exception Querying All Tasks:\n{e}")
                return []
                
    def list_task_by_id(self, task_id: str) -> Optional[TaskResponse]:
        """
        List a single task from the database

        Params:
            - task_id: str - the string representation of the task's UUID

        Returns:
            - Optional[TaskResponse]
        """

        with get_db() as db:
            try:
                task_uuid = UUID(task_id)

            except ValueError:
                self.logger.error(f"Invalid UUID Format: {task_id}")
                return None

            try:            
                found_task = (
                    db
                    .query(Task)
                    .filter(Task.id == task_uuid)
                    .first()
                )

                if not found_task:
                    return None

                return TaskResponse(
                    id = str(found_task.id),
                    task = found_task.task,
                    is_completed = found_task.is_completed,
                    created_at = found_task.created_at,
                    updated_at = found_task.updated_at
                )
            
            except Exception as e:
                self.logger.error(f"Unknown Exception Querying Single Task:\n{e}")
                return None