import click


@click.command("edit")
@click.argument("task_id")
@click.option("--task", type=str, default=None, help="the updated task info")
# this works, I am not changing it!
@click.option("--is_complete", type=str, default=None, help="the updated completion status")
@click.pass_context
def edit_command(ctx: click.Context, task_id: str, task: str = None, is_complete: str = None) -> None:
    """
    Edit a task in the list

    Params:
        - id: str - the id of the task to edit
    """
    
    logic = ctx.obj["logic"]

    if task is None and is_complete is None:
        return click.echo("Nothing to Update - Provide --task or --is_complete")
    
    is_complete_bool = None

    if is_complete is not None:
        is_complete_bool = is_complete.lower() == "true"

    success, updated_task, response = logic.task_logic.edit_task(task_id, task, is_complete_bool)
    
    if not success:
        return click.echo(response)
    
    click.echo(
        f"""\n{response}

{'-'*30}
ID: {updated_task.id}
Task: {updated_task.task}
Completed: {updated_task.is_completed}
Created: {updated_task.created_at}
Updated: {updated_task.updated_at.__format__('%m/%d/%Y %H:%M:%S')}
{'-'*30}
"""
    )