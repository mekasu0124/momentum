from PySide6.QtWidgets import QMessageBox
from typing import Tuple, List, Union
from pathlib import Path
from uuid import UUID

from .database.db import get_db, get_engine, get_base
from .models.task import Task

import json
import os
import sys


class Logic:
	def __init__(self, app_dir: Path):
		self.app_dir = app_dir
		self.config_file = f"{app_dir}/config.json"
		self.setup_environment()
		self.db = None
		
	def get_db_session(self):
		if not self.db:
			self.db = next(get_db())
			
		return self.db
		
	def close_db_session(self):
		if self.db:
			self.db.close()
			self.db = None
			
	def setup_environment(self):
		try:
			with open(self.config_file, 'r', encoding="utf-8-sig") as f:
				data = json.load(f)
				
			if data.get("agree") != 1:
				self.get_user_agreement()
				self.init_db()
		
		except FileNotFoundError:
			self.get_user_agreement()
			self.init_db()
			
		except (KeyError, json.JSONDecodeError):
			if Path(self.config_file).exists():
				os.remove(self.config_file)
				
			self.get_user_agreement()
			self.init_db()
			
	def update_user_config(self):
		try:
			Path(self.app_dir).mkdir(parents=True, exist_ok=True)
			
			with open(self.config_file, 'w', encoding="utf-8-sig") as new:
				json.dump({"agree": 1}, new, indent=2)

			self.init_db()
				
		except PermissionError:
			QMessageBox.warning(
				None,
				"Momentum - Invalid Permissions",
				(
					"Momentum failed to created the applications needed directory "
					"due to permission issues."
				)
			)
			sys.exit()
			
	def get_user_agreement(self):
		response = QMessageBox.question(
			None,
			"Momentum - Read/Write Permissions",
			(
				"Momentum requires read/write permissions to create and "
				"maintain the database that holds your entries. This "
				"application cannot run without this permission."
			),
			QMessageBox.Yes | QMessageBox.No,
			QMessageBox.Yes
		)
		
		if response == QMessageBox.No:
			QMessageBox.warning(
				None,
				"Momentum - Read/Write Permissions Denied",
				(
					"\nYou declined the user agreement. This application "
					"cannot run without this permission. If you change your mind later, "
					"run any command again."
				)
			)
			sys.exit()
		
		else:
			self.update_user_config()
			
	def init_db(self):
		get_base().metadata.create_all(bind=get_engine())

	def get_all_tasks(self) -> Union[List[Task], None]:
		db = self.get_db_session()

		try:
			all_tasks = db.query(Task).all()

			if not all_tasks or len(all_tasks) == 0:
				return []
			
			return all_tasks
		
		except Exception as e:
			print(f"Unknown Error Querying All Tasks:\n{e}")
			return None
		
		finally:
			db.close()

	def save_task(self, task_data) -> Tuple[bool, str]:
		if not task_data:
			return True, "New Task Data Cannot Be Empty"
		
		db = self.get_db_session()

		try:
			found_task = (
				db
				.query(Task)
				.filter(Task.content == task_data)
				.first()
			)

			if found_task:
				return True, "Task Already Exists"
			
			new_task = Task(content=task_data)

			db.add(new_task)
			db.commit()
			return False, "Task Saved Successfully"
		
		except Exception as e:
			print(f"Unknown Exception Saving Task:\n{e}")
			return True, "Failed to Save Task"
		
		finally:
			db.close()

	def delete_task(self, task_id) -> Tuple[bool, str]:
		if not task_id:
			return True, "Task ID Cannot Be Empty or Null!"
		
		db = self.get_db_session()

		try:
			found_task = (
				db
				.query(Task)
				.filter(Task.id == task_id)
				.first()
			)

			if not found_task:
				return True, f"No Task Found By ID: {task_id}"
			
			db.delete(found_task)
			db.commit()
			return False, "Task Deleted Successfully"
		
		except Exception as e:
			print(f"Unknown Exception Deleting Task:\n{e}")
			return True, "Failed to Delete Task"
		
		finally:
			db.close()