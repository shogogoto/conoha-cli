"""おためしCLI."""

import click
from click_shell import shell

from conoha_client.features import sshkey_cli, vm_cli


# @click.group()
@shell(prompt="(conoha-client) ")
def cli() -> None:
    """root."""


@click.command()
@click.option("--greet", help="word to greet", default="hello")
@click.argument("to")
def greet(greet: str, to: str) -> None:
    """お試しCLI."""
    click.echo(f"{greet} {to}")


def main() -> None:
    """CLI設定用."""
    cli.add_command(greet)
    cli.add_command(vm_cli)
    cli.add_command(sshkey_cli)
    cli()