"""ssh鍵CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features._shared.view.domain import view_options

from .repo import create_keypair, find_all

if TYPE_CHECKING:
    from conoha_client.features.sshkey.domain import KeyPair


@click.group(name="sshkey")
def sshkey_cli() -> None:
    """キーペアCRUD."""


@sshkey_cli.command(name="ls")
@view_options
def _list() -> list[KeyPair]:
    """キーペア一覧."""
    return find_all()
    # view(models, keys=None, style="json")
    # view(models, keys={"name"}, style="table")
    # return None


@sshkey_cli.command()
@click.option("--out-dir", help="鍵のファイル出力先", default="./")
def create(out_dir: str) -> None:
    """秘密鍵生成."""
    kp = create_keypair()
    kp.write(out_dir)
    msg = f"{kp.name}の公開鍵を登録し、秘密鍵をファイル出力しました"
    click.echo(msg)


@sshkey_cli.command()
def remove() -> None:
    """登録済み公開鍵削除."""
    body = click.get_text_stream("stdin").read()
    click.echo("###############")
    click.echo(body)
