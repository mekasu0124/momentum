import json
import sys
import os

from ..database.db import get_base, get_engine
from ..models.task import Task


class ConfigLogic:
    def __init__(self, parent=None):
        self.config = parent.config
        self.config_file = parent.config_file
        self.logger = parent.logger

    def init_environment(self) -> None:
        """
        Initializes the applications environment by 
        checking the applications directory for a config.json
        file and if it doesn't exist, or the needed permissions
        do not equal 1 upon the check, trigger get user agreement
        functionality
        
        Params:
            - None
            
        Returns:
            - None
        """

        if not self.config_file.exists():
            self.get_user_agreement()

        else:
            self.check_user_agreement()

    def check_user_agreement(self) -> None:
        """
        Checks the applications config.json file for the 
        applications needed permissions. If the permissions
        do not equal 1, trigger get user agreement, otherwise,
        initialize the database.

        Params:
            - None
        
        Returns:
            - None
        """

        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            if not data.get("rw_perms") == 1:
                self.get_user_agreement()

            else:
                self.init_db()

        except FileNotFoundError:
            self.logger.error(f"File Not Found: '{self.config_file}'")
            self.get_user_agreement()

        except (KeyError, json.JSONDecodeError):
            self.logger.error(f"Config File is Corrupt. Deleteing and re-creating... Please Wait...")

            if self.config_file.exists():
                os.remove(self.config_file)

            self.get_user_agreement()

        except Exception as e:
            self.logger.error(f"Unknown Exception Reading System Config:\n{e}")
            sys.exit(1)

    def get_user_agreement(self) -> None:
        """
        prompt the user in the console for read/write
        permissions. If accepted, update the applications
        config file, otherwise, tell the user they denied
        and exit the application.

        Params:
            - None

        Returns:
            - None
        """

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
            self.logger.error("\nInvalid Input. 'Y' for Yes or 'N' for No\n\n")

            user_agree = input(prompt)

            if user_agree in valid_options:
                break

        if user_agree.lower() == 'n':
            self.logger.error(
                "You denied the read/write permissions for this "
                "application. If you change your mind in the future, "
                "run this command again."
            )
            sys.exit(0)

        else:
            self.update_user_config()

    def update_user_config(self) -> None:
        """
        Update the applications config.json file to reflect
        the user's agreement to the read/write permissions

        Params:
            - None

        Returns:
            - None
        """
        self.config.ensure_directories()

        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            data["rw_perms"] = 1

            with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                json.dump(data, new, indent=2)

            os.chmod(self.config_file, 0o600)
            self.init_db()

        except FileNotFoundError:
            self.logger.error("config file not found. creating new config file... please wait...")
            try:
                with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                    json.dump({"rw_perms": 1}, new, indent=2)

                os.chmod(self.config_file, 0o600)
                self.init_db()

            except Exception as e:
                self.logger.error(f"Unknown Exception Creating Config File:\n{e}")
                sys.exit(1)

        except (KeyError, json.JSONDecodeError):
            self.logger.error('Config File is Corrupt. Deleting and re-creating... please wait...')

            if self.config_file.exists():
                os.remove(self.config_file)

            with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                json.dump({"rw_perms": 1}, new, indent=2)

            os.chmod(self.config_file, 0o600)
            self.init_db()

        except Exception as e:
            self.logger.error(f"Unknown Exception Updating User Config:\n{e}")
            sys.exit(1)

    def init_db(self) -> None:
        """
        Initialize the database

        Params:
            - None

        Returns:
            - None
        """

        get_base().metadata.create_all(
            bind=get_engine()
        )