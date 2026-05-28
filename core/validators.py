from .config import Config


def validate_task_name(task: str) -> bool:
    """
    Validate task name against business rules

    Params:
        - task: str - the task string to validate

    Returns:
        - bool: True if valid, False if not
    """

    if not task:
        return False
    
    stripped = task.strip()

    if not stripped:
        return False
    
    if len(stripped) < Config.MIN_TASK_LENGTH:
        return False
    
    if len(stripped) > Config.MAX_TASK_LENGTH:
        return False
    
    return True
