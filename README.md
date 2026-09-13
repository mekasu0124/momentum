# momentum

A Flask web application.

## Environment Setup

This project uses `python-dotenv` to manage environment variables. Configuration is loaded from the `.env` file.

### Environment Variables

- `SECRET_KEY`: Flask secret key for session management (change in production!)
- `FLASK_ENV`: Environment setting (development/production)
- `FLASK_DEBUG`: Enable debug mode (1/0, true/false)
- `FLASK_HOST`: Server host (default: 0.0.0.0)
- `FLASK_PORT`: Server port (default: 5000)
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disable Flask-SQLAlchemy modification tracking

Copy `.env.example` to `.env` and update values as needed:

```bash
cp .env.example .env
```

## Installation

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

```bash
momentum
```

Visit http://localhost:5000

## Installation Commands

```bash
uv init
uv venv .venv
source .venv/bin/activate
uv add flask flask-sqlalchemy python-dotenv
```

## Notes

- Database is SQLite stored in `instance/app.db`
- Templates use Jinja2 syntax
- Static files served from `static/` directory
- Debug mode enabled for development
- Environment variables are loaded from `.env` file via `python-dotenv`
