from typing import Dict, List


def format_authors(authors: List[Dict]) -> List[str]:
    """
    Format the list of authors
    
    from
        authors = [{ name: "", email: "" }]

    to
        authors = ["name (email)"]
    """

    author_list = []

    for author in authors:
        name = author.get("name", "Unknown")
        email = author.get("email", "no email")

        formatted_string = f"{name} ({email})"
        author_list.append(formatted_string)

    return author_list

def format_dependencies(dependencies: List[str]) -> List[str]:
    """
    Format the list of dependencies

    from
        dependencies = ["name==version", "git+https://..."]
    
    to
        dependencies = ["name: version"] for those with ==,
        otherwise keep original string.
    """

    dependency_list = []

    for dependency in dependencies:
        if "==" in dependency:
            name, version = dependency.split("==", 1)
            formatted_string = f"{name}: {version}"

        else:
            formatted_string = dependency

        dependency_list.append(formatted_string)

    return dependency_list

def format_scripts(scripts: Dict[str, str]) -> List[str]:
    """
    Format the list of scripts that starts each gui part

    from
        scripts = {"cli": "cmd1", "tui": "cmd2", ...}

    to
        lines = [
        "- cli tool",
        "  - cli: cmd1",
        "- tui app",
        "  - tui: cmd2",
        ...
        ]
    """

    if not scripts:
        return ["- No Scripts Configured"]

    # I am not changing this line. I am aware these slots are hard-coded. These are what they will be
    # named and these will always only be the only call signs. I am the single-dev on this project
    slots = ["momentum", "momentum-tui", "momentum-desktop", "momentum-mobile", "momentum-web"]
    scripts_list = []

    # Convert dict to lists once for efficiency
    script_names = list(scripts.keys())
    script_cmds = list(scripts.values())

    for index, slot in enumerate(slots):
        if index < len(scripts):
            cmd = script_cmds[index]
            name = script_names[index]
        else:
            cmd = "undefined"
            name = "___"

        scripts_list.append(f"- {slot}")
        scripts_list.append(f"  - {name}: executes {cmd}")

    return scripts_list