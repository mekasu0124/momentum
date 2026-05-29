import click

from .commands.hello import hello_command
from .commands.add import add_command
from .commands.edit import edit_command
from .commands.delete import delete_command
from .commands.list import list_command

from core.logic import Logic


@click.group()
@click.pass_context
def cli(ctx):
    """Entry Point for CLI Application"""
    
    ctx.ensure_object(dict)
    ctx.obj['logic'] = Logic()


cli.add_command(hello_command)
cli.add_command(add_command)
cli.add_command(edit_command)
cli.add_command(delete_command)
cli.add_command(list_command)


if __name__ == '__main__':
    cli()