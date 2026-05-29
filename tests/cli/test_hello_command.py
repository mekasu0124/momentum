from apps.cli.cli import cli


def test_hello_command(runner):
    """Test that the hello command displays without a passed user"""

    result = runner.invoke(cli, ["hello"])

    assert result.exit_code == 0
    assert result.output.strip().split('\n')[0] == "Hi, User 👋! Welcome to Momentum!"


def test_hello_command_with_user(runner):
    """Test that the hello command displays with a passed user"""

    result = runner.invoke(cli, ["hello", "--user", "test_user123"])

    assert result.exit_code == 0
    assert result.output.strip().split('\n')[0] == "Hi, test_user123 👋! Welcome to Momentum!"