from typing import Dict, Any, Tuple, Optional

from ..database.db import get_base
from ..schemas.user import UserCreate, UserUpdate, UserResponse


Base = get_base()


class UserLogic:
    def __init__(self, parent=None):
        self.parent = parent

    def create_user(self, user_dict: Dict[str, Any]) -> Tuple[bool, Optional[UserResponse], str]:
        pass