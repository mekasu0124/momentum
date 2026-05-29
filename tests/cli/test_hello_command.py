from click.testing import CliRunner
from pathlib import Path

import pytest
import tempfile

from apps.cli.cli import cli
from core.config import Config


def test_hello_command(monkeypatch):
    """Test that the hello command displays without a passed user"""

    tmpdir = tempfile.mkdtemp()
    monkeypatch.setattr(Config, "APP_DIR", Path(tmpdir))

    runner = CliRunner()
    result = runner.invoke(cli, ["hello"])

    assert result.exit_code == 0
    assert result.output.strip().split('\n')[0] == "Hi, User 👋! Welcome to Momentum!"


def test_hello_command_with_user(monkeypatch):
    """Test that the hello command displays with a passed user"""

    tmpdir = tempfile.mkdtemp()
    monkeypatch.setattr(Config, "APP_DIR", Path(tmpdir))

    runner = CliRunner()
    result = runner.invoke(cli, ["hello", "--user", "test_user123"])

    assert result.exit_code == 0
    assert result.output.strip().split('\n')[0] == "Hi, test_user123 👋! Welcome to Momentum!"