import click


@click.command("add")
@click.argument("task")
@click.pass_context
def add_command(ctx: click.Context, task: str) -> None:
    """
    Add a new task to the list

    Params:
        - ctx: ctx.ClickContext - click context passing the logic class
        - task: str - the task to add

    Returns:
        - None
    """

    if not task:
        click.echo("Task cannot be empty")
        return
    
    logic = ctx.obj["logic"]
    response = logic.add_task(task)
    click.echo(response)
    all_tasks = logic.list_tasks()

    for task in all_tasks:
        click.echo(
            f"{'-'*30}\n"
            f"ID: {task.id}\n"
            f"Task: {task.task}\n"
            f"Completed: {task.is_completed}\n"
            f"Created: {task.created_at}\n"
            f"{'-'*30}"
        )