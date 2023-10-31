"""ssh鍵CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features._shared import each_args, view_options

from .repo import create_keypair, find_all, remove_keypair

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


@sshkey_cli.command()
@click.option(
    "--out-dir",
    help="鍵のファイル出力先",
    default="./",
    show_default=True,
)
def add(out_dir: str) -> None:
    """秘密鍵生成."""
    kp = create_keypair()
    kp.write(out_dir)
    msg = f"{kp.name}の公開鍵を登録し、秘密鍵をファイル出力しました"
    click.echo(msg)


@sshkey_cli.command(name="rm")
@each_args("names")
def remove(name: str) -> None:
    """登録済み公開鍵削除."""
    remove_keypair(name)
    click.echo(f"{name} was deleted")
