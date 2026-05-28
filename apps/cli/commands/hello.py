import click

from ..utils.formats import (
    format_dependencies,
    format_authors,
    format_scripts
)


@click.command("hello")
@click.option("--user", type=str, default="User", help="the user to greet")
@click.pass_context
def hello_command(ctx: click.Context, user: str) -> None:
    """
    Welcome the user and display project information
    from pyproject.toml.
    """

    logic = ctx.obj["logic"]
    all_project_data = logic.get_pyproject_data()

    project_data = all_project_data.get("project", {})
    url_data = all_project_data.get("urls", {})
    script_data = all_project_data.get("scripts", {})

    project_name = project_data.get("name", "Unknown").capitalize()
    description = project_data.get("description", "No description provided.")
    version = project_data.get("version", "0.0.0")
    readme = project_data.get("readme", "README.md")
    requires_python = project_data.get("requires-python", "any")
    license_info = project_data.get("license", "unlicensed")

    authors = format_authors(project_data.get("authors", []))
    deps = format_dependencies(project_data.get("dependencies", []))

    homepage = url_data.get("Homepage", "not set")
    repository = url_data.get("Repository", "not set")
    documentation = url_data.get("Documentation", "not set")

    scripts_lines = format_scripts(script_data)

    response = f"""
Hi, {user} 👋! Welcome to Momentum!

{description}

🏗️ Project 🏗️
-------------
Name: {project_name}
Version: {version}
Read Me: {readme}
Python Version: {requires_python}
License: {license_info}
Authors:
  - {'\n  - '.join(authors) if authors else 'none listed'}
Dependencies:
  - {'\n  - '.join(deps) if deps else 'none'}

🔗 URLS 🔗
----------
Homepage: {homepage}
Repository: {repository}
Documentation: {documentation}

📜 Scripts 📜
-------------
Each script below runs a different client variation of {project_name}.

{chr(10).join(scripts_lines)}
"""
    click.echo(response)