"""Revenue Holdings unified CLI entry point."""

import builtins as _builtins
import subprocess
import sys
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from revenueholdings import __version__, TOOLS

app = typer.Typer(
    name="rh",
    help="Revenue Holdings — unified CLI for developer tools.",
    rich_markup_mode="rich",
)
console = Console()


def _show_version(value: bool) -> None:
    if value:
        console.print(f"[bold]rh[/] v{__version__} — Revenue Holdings CLI")
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
    name: Optional[str] = typer.Argument(None, help="Show details for a specific tool."),
):
    """List available Revenue Holdings CLI tools."""
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
                title=f"rh {name}",
            )
        )
    else:
        table = Table(title="Revenue Holdings CLI Tools")
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
        console.print(f"\n[dim]Install individually:[/dim] [green]pip install revenueholdings[guard][/green]")
        console.print(f"[dim]Install all:[/dim] [green]pip install revenueholdings[all][/green]")


@app.command()
def install(
    tool: str = typer.Argument(
        ..., help="Tool to install: " + ", ".join(TOOLS.keys()) + ", or 'all'"
    ),
):
    """Install a Revenue Holdings tool."""
    if tool == "all":
        targets = _builtins.list(TOOLS.keys())
        extras = ",".join(TOOLS.keys())
    elif tool in TOOLS:
        targets = [tool]
        extras = tool
    else:
        console.print(f"[red]Unknown tool: {tool}[/red]")
        console.print(f"Available: {', '.join(TOOLS.keys())}, 'all'")
        raise typer.Exit(code=1)

    pkg = f"revenueholdings[{extras}]"
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
        raise typer.Exit(code=1)


@app.command(name="versions")
def show_versions(
    tool: Optional[str] = typer.Argument(None, help="Check version of a specific tool."),
):
    """Show installed tool versions."""
    if tool:
        targets = [tool] if tool in TOOLS else []
    else:
        targets = _builtins.list(TOOLS.keys())
    
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


# Dynamically add subcommands for each tool
def _make_dispatch(tool_name: str):
    """Create a typer command that dispatches to the underlying tool CLI."""
    pkg = TOOLS[tool_name]["package"]

    def dispatch(
        ctx: typer.Context,
        args: List[str] = typer.Argument(None, help="Arguments to pass to the tool."),
    ):
        info = TOOLS.get(tool_name)
        if not info:
            console.print(f"[red]Unknown tool: {tool_name}[/red]")
            raise typer.Exit(code=1)

        try:
            result = subprocess.run(
                [sys.executable, "-m", info["package"].replace("-", "_")] + (args or []),
                capture_output=False,
            )
            sys.exit(result.returncode)
        except FileNotFoundError:
            console.print(
                f"[red]Tool '{tool_name}' not installed.[/red]\n"
                f"Install with: [green]pip install revenueholdings[{tool_name}][/green]"
            )
            raise typer.Exit(code=1)

    dispatch.__name__ = tool_name
    dispatch.__doc__ = f"Run `{pkg}` commands via the {tool_name} subcommand."
    return dispatch


for cmd_name in TOOLS:
    app.command(name=cmd_name)(_make_dispatch(cmd_name))


def main():
    app()


if __name__ == "__main__":
    main()
