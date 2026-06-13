"""DevForge unified CLI entry point."""

import importlib.util
import subprocess
import sys
import typer
from devforge import TOOLS, __version__
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    name="devforge",
    help="DevForge — unified CLI for developer tools.",
    rich_markup_mode="rich",
)
console = Console()


def _show_version(value: bool) -> None:
    if value:
        console.print(f"[bold]devforge[/] v{__version__} — DevForge CLI")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show version and exit.",
        callback=_show_version,
        is_eager=True,
    ),
):
    pass


@app.command(name="tools")
def list_tools(
    name: str | None = typer.Argument(None, help="Show details for a specific tool."),
):
    """List available DevForge CLI tools."""
    if name:
        tool = TOOLS.get(name)
        if not tool:
            console.print(f"[red]Unknown tool: {name}[/red]")
            raise typer.Exit(code=1)
        console.print(
            Panel.fit(
                f"[bold]{tool['icon']} {name}[/bold]\n"
                f"Package: [cyan]{tool['package']}[/cyan]\n"
                f"Description: {tool['description']}\n"
                f"Pricing: [yellow]{tool['pricing']}[/yellow]\n"
                f"Status: [green]{tool['status']}[/green]\n"
                f"URL: {tool['url']}",
                title=f"devforge {name}",
            )
        )
    else:
        table = Table(title="DevForge CLI Tools")
        table.add_column("Command", style="cyan")
        table.add_column("Package", style="green")
        table.add_column("Description")
        table.add_column("Pricing", style="yellow")
        table.add_column("Status", style="bold")

        for cmd, tool in TOOLS.items():
            table.add_row(
                tool["icon"] + " " + cmd,
                tool["package"],
                tool["description"],
                tool["pricing"],
                "✅" if tool["status"] == "ready" else tool["status"],
            )

        console.print(table)
        console.print("\n[dim]Install individually:[/dim] [green]pip install devforge[guard][/green]")
        console.print("[dim]Install all:[/dim] [green]pip install devforge[all][/green]")


@app.command()
def install(
    tool: str = typer.Argument(
        ..., help="Tool to install: " + ", ".join(TOOLS.keys()) + ", or 'all'"
    ),
):
    """Install a DevForge tool."""
    if tool == "all":
        targets = list(TOOLS.keys())
        extras = "all"
    elif tool in TOOLS:
        targets = [tool]
        extras = tool
    else:
        console.print(f"[red]Unknown tool: {tool}[/red]")
        console.print(f"Available: {', '.join(TOOLS.keys())}, 'all'")
        raise typer.Exit(code=1)

    pkg = f"devforge[{extras}]"
    console.print(f"[yellow]Installing {pkg}...[/yellow]")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            console.print(f"[green]Successfully installed:[/green] {', '.join(targets)}")
        else:
            console.print(f"[red]Installation failed:[/red] {result.stderr[:500]}")
            raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1) from e


@app.command(name="versions")
def show_versions(
    tool: str | None = typer.Argument(None, help="Check version of a specific tool."),
):
    """Show installed tool versions."""
    if tool is not None and tool not in TOOLS:
        console.print(f"[red]Unknown tool: {tool}[/red]")
        console.print(f"Available: {', '.join(TOOLS.keys())}")
        raise typer.Exit(code=1)
    targets = [tool] if tool else list(TOOLS.keys())

    for t in targets:
        info = TOOLS[t]
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", info["package"]],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.startswith("Version:"):
                        ver = line.split(":", 1)[1].strip()
                        console.print(f"[cyan]{t:8}[/cyan] v{ver}")
                        break
            else:
                console.print(f"[dim]{t:8}[/dim] [red]not installed[/red]")
        except Exception:
            console.print(f"[dim]{t:8}[/dim] [red]error checking[/red]")


def _is_tool_installed(module_name: str) -> bool:
    """Return True if the module (Python package) is importable."""
    return importlib.util.find_spec(module_name) is not None


# Dynamically add subcommands for each tool
def _make_dispatch(tool_name: str):
    """Create a typer command that dispatches to the underlying tool CLI."""
    pkg = TOOLS[tool_name]["package"]

    def dispatch(
        args: list[str] = typer.Argument(None, help="Arguments to pass to the tool."),  # noqa: B008
    ):
        info = TOOLS.get(tool_name)
        if not info:
            console.print(f"[red]Unknown tool: {tool_name}[/red]")
            raise typer.Exit(code=1)

        module_name = info["package"].replace("-", "_")
        if not _is_tool_installed(module_name):
            console.print(
                f"[red]Tool '{tool_name}' is not installed.[/red]\n"
                f"Run: [green]pip install devforge\\[{tool_name}][/green]"
            )
            raise typer.Exit(code=1)

        result = subprocess.run(
            [sys.executable, "-m", module_name] + (args or []),
            capture_output=False,
        )
        sys.exit(result.returncode)

    dispatch.__name__ = tool_name
    dispatch.__doc__ = f"Run `{pkg}` commands via the {tool_name} subcommand."
    return dispatch


for cmd_name in TOOLS:
    app.command(name=cmd_name)(_make_dispatch(cmd_name))


def main():
    app()


if __name__ == "__main__":
    main()
