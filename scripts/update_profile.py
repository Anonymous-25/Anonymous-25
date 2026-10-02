#!/usr/bin/env python3

from pathlib import Path
import re
import yaml


ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
LEARNING = ROOT / "learning.yml"


def load_config():
    with LEARNING.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def replace_section(text, name, content):
    pattern = re.compile(
        rf"(<!-- START:{name} -->).*?(<!-- END:{name} -->)",
        re.DOTALL,
    )

    replacement = (
        rf"\1\n\n"
        f"{content.strip()}\n\n"
        rf"\2"
    )

    updated, count = pattern.subn(replacement, text)

    if count != 1:
        raise RuntimeError(
            f"Could not find exactly one generated section: {name}"
        )

    return updated


def inline(items):
    return " · ".join(f"`{item}`" for item in items)


def build_learning(config):
    currently = config.get("currently_learning", [])
    security = config.get("security", {})

    tools = security.get("tools", [])
    platforms = security.get("platforms", [])

    return (
        "**Currently**\n\n"
        f"{inline(currently[:5])}\n\n"
        "**Security**\n\n"
        f"{inline(tools[:4])}\n"
        f"{inline(platforms[:3])}"
    )


def build_projects(config):
    projects = config.get("projects", [])

    names = [
        project["name"]
        for project in projects
        if project.get("status") != "Archived"
    ]

    return " · ".join(f"`{name}`" for name in names[:6])


def main():
    config = load_config()

    readme = README.read_text(encoding="utf-8")

    readme = replace_section(
        readme,
        "LEARNING",
        build_learning(config),
    )

    readme = replace_section(
        readme,
        "PROJECTS",
        build_projects(config),
    )

    README.write_text(readme, encoding="utf-8")

    print("Profile README updated successfully.")


if __name__ == "__main__":
    main()