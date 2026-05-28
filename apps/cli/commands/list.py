import click


@click.command("list")
@click.option("--task_id", type=str, default="", help="the id of the task to view")
@click.pass_context
def list_command(ctx: click.Context, task_id: str) -> None:
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
        all_tasks = logic.task_logic.list_tasks()

        if not all_tasks:
            return click.echo("No Tasks Currently Exist.")
        
        for task in all_tasks:
            if not task:
                continue

            click.echo('-'*30)
            click.echo(f"ID: {task.id}")
            click.echo(f"Task: {task.task}")
            click.echo(f"Completed: {task.is_completed}")
            click.echo(f"Created: {task.created_at.__format__('%m/%d/%Y %H:%M:%S')}")

            if task.updated_at:
                click.echo(f"Updated: {task.updated_at.__format__('%m/%d/%Y %H:%M:%S')}")

            click.echo('-'*30 + '\n')
    
    else:
        found_task = logic.task_logic.list_task_by_id(task_id)

        if not found_task:
            return click.echo(f"No Task Found By ID: {task_id}")

        click.echo('-'*30)
        click.echo(f"ID: {found_task.id}")
        click.echo(f"Task: {found_task.task}")
        click.echo(f"Completed: {found_task.is_completed}")
        click.echo(f"Created: {found_task.created_at.__format__('%m/%d/%Y %H:%M:%S')}")

        if found_task.updated_at:
            click.echo(f"Updated: {found_task.updated_at.__format__('%m/%d/%Y %H:%M:%S')}")

        click.echo('-'*30 + '\n')