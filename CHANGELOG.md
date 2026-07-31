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
  - created models directory
    - `User` model (schema only)
    - `Task` model (schema only)
    - `TaskGraveyard` model (schema only)
  - created schemas directory
    - `UserCreate`, `UserUpdate`, `UserResponse`
    - `TaskCreate`, `TaskUpdate`, `TaskResponse`
    - `TaskGraveyardCreate`, `TaskGraveyardResponse`, `TaskGraveyardRestore`
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

[Top](#top)