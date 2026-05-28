import click


@click.command("delete")
@click.argument("task_id")
@click.pass_context
def delete_command(ctx: click.Context, task_id: str) -> None:
    """
    Delete a task from the list
    
    Params:
        - ctx: click.Context - click context passing the logic class
        - task_id: str - the string representation of the tasks UUID ID

    Returns:
        - None
    """

    logic = ctx.obj["logic"]
    response = logic.delete_task(task_id)
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