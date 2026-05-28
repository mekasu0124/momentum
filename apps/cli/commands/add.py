import click


@click.command("add")
@click.argument("task", type=str)
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
    
    logic = ctx.obj["logic"]
    success, task, response = logic.task_logic.add_task(task)

    if task is None:
        return click.echo("Task Cannot Be Empty")

    if not success:
        return click.echo(response)
    
    click.echo(
        f"""\n{response}

{'-'*30}
ID: {task.id}
Task: {task.task}
Completed: {task.is_completed}
Created: {task.created_at.__format__('%m/%d/%Y %H:%M:%S')}
{'-'*30}
"""
    )