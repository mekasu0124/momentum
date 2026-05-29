from pathlib import Path
from typing import Dict, Any

import tomllib
import logging

from .config import Config
from .logic_parts.config import ConfigLogic
from .logic_parts.task import TaskLogic


class Logic:
    def __init__(self):
        self.config = Config
        self.config_file = self.config.CONFIG_PATH
        self.logger = self.configure_logger()

        self.config_logic = ConfigLogic(self)
        self.task_logic = TaskLogic(self)

        self.config_logic.init_environment()

    def configure_logger(self):
        logger = logging.getLogger(__name__)

        if not logger.handlers:
            handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

        return logger

    def get_pyproject_data(self) -> Dict[str, Any]:
        """
        Open and read the pyproject.toml file located
        at the root level of the project, gather and format
        its data and return it back to the client

        Params:
            - None

        Returns:
            - my_dict: Dict[str, Any]
        """

        pyproject_path = None

        possible_paths = [
            Path(__file__).parent.parent / "pyproject.toml",
            Path.cwd() / "pyproject.toml"
        ]

        for path in possible_paths:
            if path.exists():
                pyproject_path = path
                break

        if not pyproject_path:
            return {}
        
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