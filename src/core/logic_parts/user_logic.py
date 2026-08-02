from typing import Dict, Tuple, Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import ValidationError
from email_validator import validate_email, EmailNotValidError

from ..database.db import get_base, get_session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserResponse


Base = get_base()
ph = PasswordHasher()


class UserLogic:
    def __init__(self, parent=None):
        self.parent = parent

    def create_user(self, user_dict: Dict[str, str]) -> Tuple[bool, Optional[UserResponse], str]:
        if not user_dict:
            return False, None, "User Dict Cannot Be Empty"

        try:
            user_data = UserCreate(**user_dict)
        except ValidationError as e:
            return False, None, f"Invalid Input: {e}"
        
        email = user_data.email
        username = user_data.username
        create_pw = user_data.cr_password
        confirm_pw = user_data.cf_password

        if not all([email, username, create_pw, confirm_pw]):
            return False, None, "All Inputs Are Required!"

        if not email:
            return False, None, "Email is Required to Reset Password if Forgotten"

        if not username:
            return False, None, "Username is Required for Account Allocation and Task Association"

        if len(username) < 3:
            return False, None, "Username must be at least 3 characters long"

        if len(username) > 50:
            return False, None, "Username cannot exceed 50 characters"

        if not create_pw or not confirm_pw:
            return False, None, "Invalid Password(s)"

        if len(create_pw) < 8:
            return False, None, "Password must be at least 8 characters long"

        if create_pw != confirm_pw:
            return False, None, "Passwords Do Not Match"

        try:
            valid_email = validate_email(email, check_deliverability=False).normalized
        except EmailNotValidError:
            return False, None, "Invalid Email Address"

        session = get_session()

        try:
            existing_user = (
                session
                .query(User)
                .filter(
                    (User.username == username) |
                    (User.email == email)
                )
                .first()
            )

            if existing_user:
                if existing_user.username == username:
                    return False, None, "Username already registered"
                
                return False, None, "Email already registered"

            hashed_password = ph.hash(create_pw)

            new_user = User(
                email=valid_email,
                username=username,
                hashed_password=hashed_password
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            user_response = UserResponse(
                id=str(new_user.id),
                email=new_user.email,
                username=new_user.username,
                created_at=new_user.created_at,
                updated_at=new_user.updated_at
            )

            return True, user_response, "User Created successfully"

        except Exception as e:
            session.rollback()
            print(f"Unknown Exception Creating New User:\n{e}")
            return False, None, f"Failed to Create User: {str(e)}"
        
        finally:
            session.close()