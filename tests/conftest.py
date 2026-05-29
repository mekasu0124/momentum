# tests/conftest.py
from pathlib import Path
from typing import Generator

import pytest
import tempfile
import json
import shutil

from click.testing import CliRunner
from core.config import Config
from core.database.db import get_base, get_engine


@pytest.fixture
def isolated_app_dir(monkeypatch) -> Generator[Path, None, None]:
    """Create an isolated app directory for each test"""
    
    # Create temporary directory
    tmpdir = tempfile.mkdtemp()
    fake_home = Path(tmpdir)
    
    # Monkeypatch Path.home() to return our temporary directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    
    # Also directly override Config class attributes
    app_dir = fake_home / ".meks-apps"
    monkeypatch.setattr(Config, "APP_DIR", app_dir)
    monkeypatch.setattr(Config, "CONFIG_DIR", app_dir / "momentum")
    monkeypatch.setattr(Config, "DB_PATH", app_dir / "main.db")
    monkeypatch.setattr(Config, "CONFIG_PATH", app_dir / "momentum" / "config.json")
    
    # Setup the directory structure
    config_dir = app_dir / "momentum"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    
    # Create config file with proper permissions
    with open(config_file, 'w') as f:
        json.dump({"rw_perms": 1}, f)
    
    yield fake_home
    
    # Cleanup - remove the temporary directory
    shutil.rmtree(fake_home, ignore_errors=True)


@pytest.fixture
def runner(isolated_app_dir):
    """Provide a Click CLI runner with isolated environment"""
    return CliRunner()