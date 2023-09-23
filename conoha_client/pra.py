"""おためしCLI."""
import click


@click.command()
@click.option("--greet", help="word to greet", default="hello")
@click.argument("to")
def cli(greet:str, to:str) -> None:
    """お試しCLI."""
    click.echo(f"{greet} {to}")

def main() -> None:
    """CLI設定用."""
    cli()
