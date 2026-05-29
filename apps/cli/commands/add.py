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
    success, task_response, response = logic.task_logic.add_task(task)

    if task_response is None or not success:
        return click.echo(response)
    
    click.echo(
        f"""\n{response}

{'-'*30}
ID: {task_response.id}
Task: {task_response.task}
Completed: {task_response.is_completed}
Created: {task_response.created_at.__format__('%m/%d/%Y %H:%M:%S')}
{'-'*30}
"""
    )