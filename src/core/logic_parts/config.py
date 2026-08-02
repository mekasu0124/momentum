from typing import Dict

import json
import os


class ConfigLogic:
    def __init__(self, parent=None):
        self.parent = parent

    def check_user_agreement(self) -> bool:
        config_path = self.parent.app_dir / "config.json"

        try:
            with open(config_path, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

        except FileNotFoundError:
            return False

        except (KeyError, json.JSONDecodeError):
            return False

        except Exception as e:
            print(f"Unknown Exception Reading Config:\n{e}")
            return False

        else:
            rw_perm = data.get("read_write", 0)
            tos_perm = data.get("tos", 0)
            ua_perm = data.get("ua", 0)

            return rw_perm == 1 and tos_perm == 1 and ua_perm == 1

    def update_agreements(self, agreement_data: Dict[str, int]) -> bool:
        if not agreement_data:
            return False

        config_path = self.parent.app_dir / "config.json"

        if not config_path.parent.exists():
            config_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(config_path, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

        except FileNotFoundError:
            data = {}

        except (KeyError, json.JSONDecodeError):
            if config_path.exists():
                os.remove(config_path)

            data = {}

        except Exception as e:
            print(f"Unknown Exception Updating Config File:\n{e}")
            return False

        data["read_write"] = agreement_data.get("read_write", 0)
        data["browser"] = agreement_data.get("browser", 0)
        data["tos"] = agreement_data.get("tos", 0)
        data["ua"] = agreement_data.get("ua", 0)

        try:
            with open(config_path, 'w+', encoding="utf-8-sig") as f:
                json.dump(data, f, indent=2)

            self.parent.init_db()

            return True

        except Exception as e:
            print(f"Unknown Exception Writing Config File:\n{e}")
            return False