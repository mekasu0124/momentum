import click


@click.command("edit")
@click.argument("task_id")
@click.argument("task")
@click.pass_context
def edit_command(ctx: click.Context, task_id: str, task: str):
    """
    Delete a task from the list

    Params:
        - id: str - the id of the task to edit
    """
    
    logic = ctx.obj["logic"]
    response = logic.edit_task(task_id, task)
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