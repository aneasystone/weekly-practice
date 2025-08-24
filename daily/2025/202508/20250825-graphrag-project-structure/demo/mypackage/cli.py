"""Command line interface for mypackage."""

import typer

app = typer.Typer(
    help="示例命令行工具",
    no_args_is_help=True,
)

@app.command("hello")
def hello_cmd(
    name: str = typer.Option(..., "--name", "-n", help="你的名字"),
    count: int = typer.Option(1, "--count", "-c", help="重复次数"),
    uppercase: bool = typer.Option(False, "--uppercase", "-u", help="是否大写"),
):
    """打招呼命令"""
    greeting = f"Hello {name}!"
    if uppercase:
        greeting = greeting.upper()

    for _ in range(count):
        typer.echo(greeting)

if __name__ == "__main__":
    app()