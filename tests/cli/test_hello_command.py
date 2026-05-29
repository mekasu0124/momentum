from click.testing import CliRunner

import pytest

from apps.cli.cli import cli


def test_hello_command():
    """Test that the hello command displays without a passed user"""

    runner = CliRunner()
    result = runner.invoke(cli, ['hello'])

    assert result.exit_code == 0
    assert result.output.strip().split('\n')[0] == "Hi, User 👋! Welcome to Momentum!"