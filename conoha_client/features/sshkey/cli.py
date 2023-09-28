"""ssh鍵CLI."""

from http import HTTPStatus
from pathlib import Path

import click

from conoha_client.features._shared import Endpoints, now_jst

from .repo import find_all


@click.group(name="sshkey")
def sshkey_cli() -> None:
    """キーペアCRUD."""


@sshkey_cli.command(name="list")
def _list() -> None:
    """キーペア一覧."""
    click.echo(find_all())


class KeyPairAlreadyExistsError(Exception):
    """既に同一名のssh公開鍵が登録されている."""


@sshkey_cli.command()
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


@sshkey_cli.command()
def remove() -> None:
    """登録済み公開鍵削除."""
    body = click.get_text_stream("stdin").read()
    click.echo("###############")
    click.echo(body)
