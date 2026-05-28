import click


@click.command("list")
@click.option("--task_id", help="the id of the task to view")
@click.pass_context
def list_command(ctx: click.Context, task_id: str = None) -> None:
    """
    List one or all tasks in the list
    
    Params:
        - ctx: click.Context - the click context passing the logic class
        - task_id: str (optional) - the id of the task to view

    Returns:
        - None
    """

    logic = ctx.obj["logic"]

    if not task_id:        
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

    else:
        task = logic.list_task_by_id(task_id)

        click.echo(
            f"{'-'*30}\n"
            f"ID: {task.id}\n"
            f"Task: {task.task}\n"
            f"Complete: {task.is_completed}\n"
            f"Created: {task.created_at}\n"
            f"{'-'*30}"
        )