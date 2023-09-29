"""VM関連 CLI定義."""

import json

import click
from flatten_dict import flatten
from tabulate import tabulate

from .server import list_servers


@click.group(name="vm")
def vm_cli() -> None:
    """VM関連."""


@vm_cli.command(name="list")
def _list() -> None:
    """契約中サーバー一覧取得コマンド."""
    res = [flatten(json.loads(s.json()), reducer="dot") for s in list_servers()]
    for s in list_servers():
        print(s.model_dump_json(indent=2))  # noqa: T201
    print(tabulate(res, headers="keys", showindex=True))  # noqa: T201
