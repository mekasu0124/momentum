from typing import Dict, Any, Tuple, Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from ..database.db import get_base, get_session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserResponse


Base = get_base()
ph = PasswordHasher()


class UserLogic:
    def __init__(self, parent=None):
        self.parent = parent

    def create_user(self, user_dict: Dict[str, Any]) -> Tuple[bool, Optional[UserResponse], str]:
        """
        Create a new user from a dictionary received from the registration form.
        
        Args:
            user_dict: Dict with keys "email", "username", "cr_password", "cf_password"
            
        Returns:
            Tuple of (success, UserResponse or None, message)
        """
        email = user_dict.get("email", "").strip()
        username = user_dict.get("username", "").strip()
        create_pw = user_dict.get("cr_password", "").strip()
        confirm_pw = user_dict.get("cf_password", "").strip()

        # Validate required fields
        if not all([email, username, create_pw, confirm_pw]):
            return (False, None, "All Inputs Are Required!")

        if not email:
            return (False, None, "Email is Required to Reset Password if Forgotten")

        if not username:
            return (False, None, "Username is Required for Account Allocation and Task Association")

        if len(username) < 3:
            return (False, None, "Username must be at least 3 characters long")

        if len(username) > 50:
            return (False, None, "Username cannot exceed 50 characters")

        if not create_pw or not confirm_pw:
            return (False, None, "Invalid Password(s)")

        if len(create_pw) < 8:
            return (False, None, "Password must be at least 8 characters long")

        if create_pw != confirm_pw:
            return (False, None, "Passwords Do Not Match")

        session = get_session()
        try:
            # Check if user already exists
            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()

            if existing_user:
                if existing_user.username == username:
                    return (False, None, "Username already registered")
                return (False, None, "Email already registered")

            # Hash the password (only need to hash one of them since they match)
            hashed_password = ph.hash(confirm_pw)

            # Create new user
            new_user = User(
                email=email,
                username=username,
                hashed_password=hashed_password
            )

            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            # Return response
            user_response = UserResponse(
                id=str(new_user.id),
                email=new_user.email,
                username=new_user.username,
                created_at=new_user.created_at,
                updated_at=new_user.updated_at
            )

            return (True, user_response, "User created successfully")

        except Exception as e:
            session.rollback()
            return (False, None, f"Failed to create user: {str(e)}")
        finally:
            session.close()

    def verify_password(self, username: str, password: str) -> Tuple[bool, Optional[User]]:
        """Verify a user's password during login."""
        session = get_session()
        try:
            user = session.query(User).filter(
                User.username == username).first()

            if not user:
                return (False, None)

            try:
                ph.verify(user.hashed_password, password)
                return (True, user)
            except VerifyMismatchError:
                return (False, None)

        finally:
            session.close()

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get a user by email."""
        session = get_session()
        try:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                return None

            return UserResponse(
                id=str(user.id),
                email=user.email,
                username=user.username,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        finally:
            session.close()

    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get a user by UUID."""
        session = get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                return None

            return UserResponse(
                id=str(user.id),
                email=user.email,
                username=user.username,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        finally:
            session.close()
