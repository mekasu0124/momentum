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
    success, response = logic.task_logic.delete_task(task_id)

    if not success:
        return click.echo(response)
    
    click.echo(response)