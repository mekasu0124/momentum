from click.testing import CliRunner
from pathlib import Path

import pytest
import tempfile
import json

from apps.cli.cli import cli
from core.config import Config


def test_add_command(monkeypatch):
    """Test the add command with no parameters"""

    # Create temporary directory to use as fake home
    tmpdir = tempfile.mkdtemp()
    fake_home = Path(tmpdir)
    
    # Monkey-patch Path.home() to return our temporary directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    
    # Setup the expected directory structure under fake home
    app_dir = fake_home / ".meks-apps"
    config_dir = app_dir / "momentum"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    
    # Create config file with proper permissions to bypass user agreement
    with open(config_file, 'w') as f:
        json.dump({"rw_perms": 1}, f)

    runner = CliRunner()
    result = runner.invoke(cli, ["add"])

    assert "Error: Missing argument 'TASK'" in result.output.strip()


def test_add_command_with_empty_value(monkeypatch):
    """Test the add command with an empty task value"""

    # Create temporary directory to use as fake home
    tmpdir = tempfile.mkdtemp()
    fake_home = Path(tmpdir)
    
    # Monkey-patch Path.home() to return our temporary directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    
    # Setup the expected directory structure under fake home
    app_dir = fake_home / ".meks-apps"
    config_dir = app_dir / "momentum"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    
    # Create config file with proper permissions to bypass user agreement
    with open(config_file, 'w') as f:
        json.dump({"rw_perms": 1}, f)

    runner = CliRunner()
    result = runner.invoke(cli, ["add", ""])

    assert result.output.strip() == "Invalid Task"


def test_add_command_with_value(monkeypatch):
    """Test the add command with a task value"""

    # Create temporary directory to use as fake home
    tmpdir = tempfile.mkdtemp()
    fake_home = Path(tmpdir)
    
    # Monkey-patch Path.home() to return our temporary directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    
    # Setup the expected directory structure under fake home
    app_dir = fake_home / ".meks-apps"
    config_dir = app_dir / "momentum"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    
    # Create config file with proper permissions to bypass user agreement
    with open(config_file, 'w') as f:
        json.dump({"rw_perms": 1}, f)

    runner = CliRunner()
    result = runner.invoke(cli, ["add", "test"])

    assert result.exit_code == 0
    assert "Task Saved Successfully" in result.output.strip().split('\n')[0]


def test_add_command_with_only_spaces(monkeypatch):
    """Test the add command with a task containing only spaces"""

    # Create temporary directory to use as fake home
    tmpdir = tempfile.mkdtemp()
    fake_home = Path(tmpdir)
    
    # Monkey-patch Path.home() to return our temporary directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    
    # Setup the expected directory structure under fake home
    app_dir = fake_home / ".meks-apps"
    config_dir = app_dir / "momentum"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    
    # Create config file with proper permissions to bypass user agreement
    with open(config_file, 'w') as f:
        json.dump({"rw_perms": 1}, f)

    runner = CliRunner()
    result = runner.invoke(cli, ["add", "   "])

    assert result.output.strip() == "Invalid Task"


def test_add_command_with_one_character(monkeypatch):
    """Test the add command with a single character task"""

    # Create temporary directory to use as fake home
    tmpdir = tempfile.mkdtemp()
    fake_home = Path(tmpdir)
    
    # Monkey-patch Path.home() to return our temporary directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    
    # Setup the expected directory structure under fake home
    app_dir = fake_home / ".meks-apps"
    config_dir = app_dir / "momentum"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    
    # Create config file with proper permissions to bypass user agreement
    with open(config_file, 'w') as f:
        json.dump({"rw_perms": 1}, f)

    runner = CliRunner()
    result = runner.invoke(cli, ["add", "a"])

    assert result.exit_code == 0
    assert "Task Saved Successfully" in result.output.strip().split('\n')[0]


def test_add_command_with_max_length(monkeypatch):
    """Test the add command with a task at maximum length (200 characters)"""

    # Create temporary directory to use as fake home
    tmpdir = tempfile.mkdtemp()
    fake_home = Path(tmpdir)
    
    # Monkey-patch Path.home() to return our temporary directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    
    # Setup the expected directory structure under fake home
    app_dir = fake_home / ".meks-apps"
    config_dir = app_dir / "momentum"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    
    # Create config file with proper permissions to bypass user agreement
    with open(config_file, 'w') as f:
        json.dump({"rw_perms": 1}, f)

    runner = CliRunner()
    max_task = "a" * 200
    result = runner.invoke(cli, ["add", max_task])

    assert result.exit_code == 0
    assert "Task Saved Successfully" in result.output.strip().split('\n')[0]


def test_add_command_with_over_max_length(monkeypatch):
    """Test the add command with a task exceeding maximum length (201 characters)"""

    # Create temporary directory to use as fake home
    tmpdir = tempfile.mkdtemp()
    fake_home = Path(tmpdir)
    
    # Monkey-patch Path.home() to return our temporary directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    
    # Setup the expected directory structure under fake home
    app_dir = fake_home / ".meks-apps"
    config_dir = app_dir / "momentum"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    
    # Create config file with proper permissions to bypass user agreement
    with open(config_file, 'w') as f:
        json.dump({"rw_perms": 1}, f)

    runner = CliRunner()
    over_task = "a" * 201
    result = runner.invoke(cli, ["add", over_task])

    assert result.output.strip() == "Invalid Task"


def test_add_command_duplicate_task(monkeypatch):
    """Test the add command with a duplicate task"""

    # Create temporary directory to use as fake home
    tmpdir = tempfile.mkdtemp()
    fake_home = Path(tmpdir)
    
    # Monkey-patch Path.home() to return our temporary directory
    monkeypatch.setattr(Path, "home", lambda: fake_home)
    
    # Setup the expected directory structure under fake home
    app_dir = fake_home / ".meks-apps"
    config_dir = app_dir / "momentum"
    config_dir.mkdir(parents=True)
    config_file = config_dir / "config.json"
    
    # Create config file with proper permissions to bypass user agreement
    with open(config_file, 'w') as f:
        json.dump({"rw_perms": 1}, f)

    runner = CliRunner()
    # First add
    result1 = runner.invoke(cli, ["add", "duplicate task"])
    assert result1.exit_code == 0
    assert "Task Saved Successfully" in result1.output.strip().split('\n')[0]

    # Second add of the same task
    result2 = runner.invoke(cli, ["add", "duplicate task"])
    assert result2.exit_code == 0
    assert result2.output.strip() == "Task Already Exists"