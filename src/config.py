from pathlib import Path

import json
import os


class Config:
    def __init__(self, app_dir: Path) -> None:
        self.app_dir = app_dir
        self.config_file = Path(f"{self.app_dir}/config.json")

    def check_user_agreement(self) -> bool:
        if not self.config_file.exists():
            return False
    
        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            return data["read_write"] == 1
        
        except (FileNotFoundError, (KeyError, json.JSONDecodeError)):
            return False
        
        except Exception as e:
            print(f"Unknown Exception Querying Config File:\n{e}")
            return False
        
    def update_user_agreement(self) -> bool:
        if not self.app_dir.exists():
            self.app_dir.mkdir(parents=True, exist_ok=True)
            
        try:
            with open(self.config_file, 'r', encoding="utf-8-sig") as f:
                data = json.load(f)

            data["read_write"] = 1

            with open(self.config_file, 'w+', encoding="utf-8-sig") as updated:
                json.dump(data, updated, indent=2)

            return True
        
        except FileNotFoundError:
            with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                json.dump({"read_write": 1}, new, indent=2)

            return True
        
        except (KeyError, json.JSONDecodeError):
            print("config file possibly corrupt. recreating file.")
            if self.config_file.exists():
                os.remove(self.config_file)

            with open(self.config_file, 'w+', encoding="utf-8-sig") as new:
                json.dump({"read_write": 1}, new, indent=2)

            return True
        
        except Exception as e:
            print(f"Unknown Exception Updating Config File:\n{e}")
            return False