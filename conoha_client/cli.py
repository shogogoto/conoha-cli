"""おためしCLI."""

import click
from click_shell import shell
from flatten_dict import flatten
from tabulate import tabulate

from conoha_client.features.keypars import tmp

from .features.list_servers import list_servers


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


@click.group()
def server() -> None:
    """server関連."""


@server.command(name="list")
def _list() -> None:
    """契約中サーバー一覧取得コマンド."""
    import json

    res = [flatten(json.loads(s.json()), reducer="dot") for s in list_servers()]
    for s in list_servers():
        print(s.model_dump_json(indent=2))  # noqa: T201
    print(tabulate(res, headers="keys", showindex=True))  # noqa: T201


@click.group()
def billing() -> None:
    """請求・課金関連."""


def main() -> None:
    """CLI設定用."""
    cli.add_command(greet)
    cli.add_command(billing)
    cli.add_command(server)
    cli.add_command(tmp)
    cli()
