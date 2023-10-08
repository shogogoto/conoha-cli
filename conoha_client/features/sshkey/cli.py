"""ssh鍵CLI."""
from __future__ import annotations

import sys
from typing import TYPE_CHECKING, TextIO

import click

from conoha_client.features._shared import view_options

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
    # view(models, keys=None, style="json")
    # view(models, keys={"name"}, style="table")
    # return None


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


# @click.argument("file", nargs=1, type=click.File("r"), default=sys.stdin)


@sshkey_cli.command(name="rm")
@click.argument("names", nargs=-1)
@click.option(
    "--file",
    "-f",
    type=click.File("r"),
    default=sys.stdin,
    help="defaultで標準入力をnamesに追加する",
)
def remove(names: tuple[str], file: TextIO) -> None:
    """登録済み公開鍵削除."""
    _names = list(names)
    if not file.isatty():
        s = file.read().splitlines()
        _names.extend(s)

    for name in _names:
        remove_keypair(name)
        click.echo(f"{name}を削除しました")
