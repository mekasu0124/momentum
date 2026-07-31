from typing import Dict

import json
import os


class ConfigLogic:
    def __init__(self, parent=None):
        self.parent = parent

    def check_user_agreement(self) -> bool:
        print("checking user agreement... please wait...")

        config_path = self.parent.app_dir / "config.json"

        try:
            with open(config_path, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

        except FileNotFoundError:
            print("config.json file not found")
            return False

        except (KeyError, json.JSONDecodeError):
            print("invalid/corrupt config.json found")
            return False

        except Exception as e:
            print(f"Unknown Exception Reading Config:\n{e}")
            return False

        else:
            print("config.json found, reading and returning agreements")
            return data.get("read_write", 0) == 1 and data.get("user_agree", 0) == 1

    def update_rw_and_browser_perms(self, updated_agreement: Dict[str, int]) -> bool:
        print("updating app permissions... please wait...")

        if not updated_agreement:
            return False

        config_path = self.parent.app_dir / "config.json"

        if not config_path.parent.exists():
            config_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(config_path, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

        except FileNotFoundError:
            print("config file not found. creating new config...")
            data = {}

        except (KeyError, json.JSONDecodeError):
            print("invalid/corrupt config file found... deleting and re-creating")
            if config_path.exists():
                os.remove(config_path)
            data = {}

        except Exception as e:
            print(f"Unknown Exception Updating Config File:\n{e}")
            return False

        data["read_write"] = updated_agreement.get("read_write", 0)
        data["browser"] = updated_agreement.get("browser", 0)

        if "user_agree" not in data:
            data["user_agree"] = 0

        try:
            with open(config_path, 'w+', encoding="utf-8-sig") as f:
                json.dump(data, f, indent=2)
            return True

        except Exception as e:
            print(f"Unknown Exception Writing Config File:\n{e}")
            return False

    def update_user_agreement(self, updated_agreement: Dict[str, int]) -> bool:
        print("updating user agreement... please wait...")

        if not updated_agreement:
            return False

        config_path = self.parent.app_dir / "config.json"

        if not config_path.parent.exists():
            config_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(config_path, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

        except FileNotFoundError:
            print("config file not found. this should not happen since TOS screen creates it first")
            return False

        except (KeyError, json.JSONDecodeError):
            print("invalid/corrupt config file found... deleting and re-creating")

            if config_path.exists():
                os.remove(config_path)

            return False

        except Exception as e:
            print(f"Unknown Exception Updating Config File:\n{e}")
            return False

        data["user_agree"] = updated_agreement.get("user_agree", 0)

        try:
            with open(config_path, 'w+', encoding="utf-8-sig") as f:
                json.dump(data, f, indent=2)

            self.parent.init_db()
            return True

        except Exception as e:
            print(f"Unknown Exception Writing Config File:\n{e}")
            return False
