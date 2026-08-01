<label id="top"></label>

Momentum CHANGELOG

Table of Contents:
- [2026](#2026)
  - [July](#july)
    - [30th](#30th)
    - [31st](#31st)

---

# 2026

## July

### 30th
- created project
- setup project with "uv init"
- setup virtual env with "uv venv .venv"
- added dependencies
  - [PySide6](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html)
  - [PySide6-Fluent-Widgets](https://qfluentwidgets.com/)
  - [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
  - [Pydantic](https://pydantic.dev/docs/validation/latest/get-started/)
  - [Python DotENV](https://github.com/theskumar/python-dotenv)
- created entry function
  - imported necessary packages/modules
  - created main application
- implemented core application structure
  - created `Logic` class in `src/core/logic.py`
    - handles app directory management
    - loads TOS and UA text files
    - initializes database
  - created `ConfigLogic` class in `src/core/logic_parts/config.py`
    - reads/writes `config.json` for user agreements
    - manages read/write and browser permissions
    - handles user agreement updates
- implemented database layer
  - created `src/core/database/db.py` with SQLAlchemy setup
    - SQLite connection with `~/.meks-apps/momentum/main.db`
    - scoped session factory for thread safety
  - created models directory with full implementations
    - `User` model with UUID primary key, email, username, hashed_password, timestamps
    - `Task` model with UUID primary key, user_id FK, title, content, timestamps
    - `TaskGraveyard` model with UUID primary key, user_id FK, title, content, timestamps
    - established relationships: One User => Many Tasks, One User => Many Graveyard Tasks
  - created schemas directory with full implementations
    - `UserCreate` with email, username, cr_password, cf_password fields and password match validation
    - `UserUpdate` with optional fields for partial updates
    - `UserResponse` with UUID, email, username, timestamps
    - `TaskCreate` with user_id, title, content
    - `TaskUpdate` with optional title, content
    - `TaskResponse` with UUID, user_id, title, content, timestamps
    - `TaskGraveyardCreate` with user_id, title, content
    - `TaskGraveyardResponse` with UUID, user_id, title, content, timestamps
    - `TaskGraveyardRestore` for restoring tasks from graveyard
- implemented `UserLogic` class in `src/core/logic_parts/user_logic.py`
  - `create_user()` with argon2 password hashing
  - validates email, username (3-50 chars), password (8+ chars)
  - checks for existing username/email before creating
  - returns `(bool, Optional[UserResponse], str)` tuple
  - `verify_password()` for login authentication
  - `get_user_by_email()` and `get_user_by_id()` for retrieval
- implemented `AsyncHelper` and `AsyncWorker` utilities
  - background threading with `QThreadPool`
  - signals for started, finished, error, progress
  - auto-cleanup with `setAutoDelete(True)`
- implemented `ApplicationManager` class
  - handles window lifecycle (show_main, show_login, show_new_user)
  - manages window switching with proper cleanup
  - connects signals between windows
- implemented new user registration flow
  - `Welcome` page with app introduction and features
  - `TOS` page with Terms of Service text and checkboxes
  - `UA` page with User Agreement text and checkbox
  - `Register` page with form for email, username, password
  - page transitions with fade animation
  - status bar messages for loading and error states
  - async loading of TOS/UA text files
  - checkbox validation before proceeding
  - registration form passes dict with email, username, cr_password, cf_password to UserLogic
- implemented login window structure
  - `LoginWindow` with `Dashboard` page
  - `new_user_requested` and `login_success` signals
  - placeholder login button for demonstration
- implemented main application window
  - `Momentum` class with `FluentWindow` inheritance
  - `Dashboard` page placeholder
  - theme and style application
  - database connection cleanup on close
- configured color theme in `src/assets/color_theme.py`
  - dark theme with cyan accent (#28E7FF)
  - comprehensive palette (background, surface, primary, secondary, text, status colors)
  - glow and shadow effects
- created `Config` class in `src/config.py`
  - `APP_DIR`: `~/.meks-apps/momentum`
  - `PROJECT_DIR`: project root
  - `ICON_PATH`: assets/app-icon.png
- wrote Terms of Service (`tos.txt`)
  - 15 sections covering license, user responsibilities, privacy, permissions, liability
- wrote User Agreement (`ua.txt`)
  - 13 sections covering local-first architecture, data ownership, security, warranty
- updated `src/main.py` entry point
  - initializes `QApplication`
  - creates `Logic`, `AsyncHelper`, `ApplicationManager`
  - checks user agreement status
  - routes to new_user or login flow
- updated `src/__init__.py` exports
- added `UserLogic` to `Logic` class initialization
- updated `src/core/schemas/__init__.py` exports with proper commas
- added `.python-version` file (Python 3.14)

### 31st
- reviewed and validated argon2 password hashing implementation
  - confirmed `ph.hash()` correctly creates hashes
  - removed redundant `ph.verify()` during user creation
  - kept `ph.verify()` for login authentication only
- updated models with foreign key relationships
  - added `user_id` ForeignKey to `Task` and `TaskGraveyard` models
  - added `ondelete="CASCADE"` for automatic cleanup
  - added `relationship()` with `back_populates` for bidirectional navigation
  - fixed inconsistent naming: `update_at` → `updated_at` across all models
- updated schemas to match client data structure
  - changed `UserCreate` schema to accept `email`, `username`, `cr_password`, `cf_password`
  - added `@model_validator` to validate passwords match
  - updated `UserResponse` schema with `email` field
  - updated `TaskCreate` and `TaskGraveyardCreate` with `user_id` field
  - fixed missing commas in `__all__` exports
- updated `UserLogic.create_user()` method
  - changed parameter from `UserCreate` schema to `Dict[str, Any]` to match client
  - added comprehensive validation for all fields
  - added username length validation (3-50 chars)
  - added password length validation (8+ chars)
  - added check for existing username or email
  - properly stores hashed password in database
  - returns `UserResponse` with UUID, email, username, timestamps
- updated CHANGELOG with all work from today

[Top](#top)