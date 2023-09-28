"""ssh用鍵関連."""

import json
from http import HTTPStatus
from pathlib import Path
from pprint import pprint

import click

from conoha_client.features._shared import Endpoints, now_jst


@click.group(name="sshkey")
def sshkey_cli() -> None:
    """キーペアCRUD."""


@sshkey_cli.command(name="list")
def _list() -> None:
    """キーペア一覧."""
    res = Endpoints.COMPUTE.get("os-keypairs").json()["keypairs"]

    click.echo(json.dumps(res, indent=2))
    names = [d["keypair"]["name"] for d in res]
    click.echo(names)


@click.command()
@click.argument("name")
def detail(name: str) -> None:
    """Xxx."""
    res = Endpoints.COMPUTE.get(f"os-keypairs/{name}").json()["keypair"]
    pprint(res)  # noqa: T203


class KeyPairAlreadyExistsError(Exception):
    """既に同一名のssh公開鍵が登録されている."""


@click.command()
def create() -> None:
    """秘密鍵生成."""
    stamp = now_jst().strftime("%Y-%m-%d-%H-%M")
    body = {"keypair": {"name": f"conoha-client-{stamp}"}}
    res = Endpoints.COMPUTE.post("os-keypairs", json=body)
    if res.status_code == HTTPStatus.CONFLICT:
        raise KeyPairAlreadyExistsError
    p = Path(f"id_rsa-{stamp}")
    click.echo(res.json())
    p.write_text(res.json()["keypair"]["private_key"])


@click.command()
def remove() -> None:
    """登録済み公開鍵削除."""


sshkey_cli.add_command(_list)
sshkey_cli.add_command(detail)
sshkey_cli.add_command(create)
sshkey_cli.add_command(remove)
