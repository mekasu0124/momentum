from apps.cli.cli import cli


def test_add_command(runner):
    """Test the add command with no parameters"""
    result = runner.invoke(cli, ["add"])
    assert "Error: Missing argument 'TASK'" in result.output.strip()


def test_add_command_with_empty_value(runner):
    """Test the add command with an empty task value"""
    result = runner.invoke(cli, ["add", ""])
    assert result.output.strip() == "Invalid Task"


def test_add_command_with_value(runner, isolated_app_dir):
    """Test the add command with a task value"""
    result = runner.invoke(cli, ["add", "test"])
    
    assert result.exit_code == 0
    assert "Task Saved Successfully" in result.output.strip().split('\n')[0]


def test_add_command_with_only_spaces(runner):
    """Test the add command with a task containing only spaces"""
    result = runner.invoke(cli, ["add", "   "])
    assert result.output.strip() == "Invalid Task"


def test_add_command_with_one_character(runner, isolated_app_dir):
    """Test the add command with a single character task"""
    result = runner.invoke(cli, ["add", "a"])
    
    assert result.exit_code == 0
    assert "Task Saved Successfully" in result.output.strip().split('\n')[0]


def test_add_command_with_max_length(runner, isolated_app_dir):
    """Test the add command with a task at maximum length (200 characters)"""
    max_task = "a" * 200
    result = runner.invoke(cli, ["add", max_task])
    
    assert result.exit_code == 0
    assert "Task Saved Successfully" in result.output.strip().split('\n')[0]


def test_add_command_with_over_max_length(runner):
    """Test the add command with a task exceeding maximum length (201 characters)"""
    over_task = "a" * 201
    result = runner.invoke(cli, ["add", over_task])
    assert result.output.strip() == "Invalid Task"


def test_add_command_duplicate_task(runner, isolated_app_dir):
    """Test the add command with a duplicate task"""
    # First add
    result1 = runner.invoke(cli, ["add", "duplicate task"])
    assert result1.exit_code == 0
    assert "Task Saved Successfully" in result1.output.strip().split('\n')[0]

    # Second add of the same task
    result2 = runner.invoke(cli, ["add", "duplicate task"])
    assert result2.exit_code == 0
    assert result2.output.strip() == "Task Already Exists"