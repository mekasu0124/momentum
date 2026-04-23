# Momentum

A modern, lightweight desktop application for efficient task tracking and management, built with PySide6 and SQLAlchemy.

## Features

- **Task Management**: Create, view, and delete tasks with ease
- **Persistent Storage**: SQLite database (configurable) for reliable data persistence
- **Modern UI**: Clean, glass-morphism design with customizable color themes
- **Async Operations**: Non-blocking database operations for smooth user experience
- **Cross-platform**: Works on Windows, macOS, and Linux

## Tech Stack

- **Frontend**: PySide6, qfluentwidgets
- **Backend**: SQLAlchemy, SQLite
- **Async**: QThreadPool for non-blocking operations
- **Language**: Python 3.12+

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/mek0124/momentum.git
cd momentum
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

### Using pip

```bash
pip install momentum
```

## Usage

### Run the application

```bash
momentum
```

Or from source:

```bash
python -m app.app
```

### First-time Setup

- The application will request permission to create a local database
- Grant access to enable task persistence
- Database is stored at `~/.momentum/main.db` (configurable via `.env`)

### Managing Tasks

1. **Add a Task**: Type your task in the input field and press Enter or click the send button
2. **Delete a Task**: Click the delete icon (trash can) next to any task
3. **View Tasks**: All tasks appear in the scrollable history widget

## Configuration

### Environment Variables

Create a `.env` file in the project root to override default settings:

```env
SQL_DB_URL=sqlite:///custom/path/to/database.db
```

### Color Theme

The application uses a customizable dark theme with teal accents. Modify `core/utils/color_theme.py` to adjust colors:

```python
COLOR_THEME = {
    "background": "#0a0c12",
    "primary": "#00c8c8",
    "text_primary": "#edf2f7",
    # ... additional color options
}
```

## Project Structure

```
momentum/
├── app/                    # Frontend application
│   ├── assets/            # Images and resources
│   ├── components/        # Reusable UI components
│   │   └── history.py     # Task history widget
│   ├── pages/             # Application pages
│   │   └── dashboard.py   # Main dashboard
│   ├── utils/             # UI utilities
│   │   └── status_bar.py  # Status bar helpers
│   └── app.py             # Main application entry
├── core/                  # Backend logic
│   ├── database/          # Database setup and session management
│   ├── models/            # SQLAlchemy models
│   │   └── task.py        # Task model
│   ├── utils/             # Core utilities
│   │   ├── async_helper.py
│   │   ├── async_worker.py
│   │   └── color_theme.py
│   └── logic.py           # Business logic
├── pyproject.toml         # Project configuration
└── README.md
```

## Development

### Running in Development Mode

```bash
python -m app.app
```

### Building from Source

```bash
pip install build
python -m build
```

### Adding New Features

1. **Database Models**: Add new models in `core/models/`
2. **UI Components**: Create widgets in `app/components/`
3. **Business Logic**: Extend `core/logic.py`
4. **Async Operations**: Use `AsyncHelper` for non-blocking database calls

## Troubleshooting

### Database Connection Issues

- Ensure the `~/.momentum/` directory has write permissions
- Check `.env` file for valid `SQL_DB_URL`

### Application Won't Start

- Verify Python 3.12+ is installed: `python --version`
- Reinstall dependencies: `pip install -e . --force-reinstall`
- Delete `~/.momentum/config.json` to reset permissions

## License

MIT License - see [LICENSE](LICENSE) file for details

## Author

**mekasu0124** - [mek0124@proton.me](mailto:mek0124@proton.me)

## Repository

- **Homepage**: [https://github.com/mek0124/momentum](https://github.com/mek0124/momentum)
- **Issues**: [https://github.com/mek0124/momentum/issues](https://github.com/mek0124/momentum/issues)

## Acknowledgments

- Built with [PySide6](https://doc.qt.io/qtforpython-6/)
- UI components from [qfluentwidgets](https://qfluentwidgets.com/)
- Database ORM by [SQLAlchemy](https://www.sqlalchemy.org/)
