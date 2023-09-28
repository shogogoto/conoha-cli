"""ssh鍵CLI."""

from pprint import pprint

import click

from .repo import create_keypair, find_all


@click.group(name="sshkey")
def sshkey_cli() -> None:
    """キーペアCRUD."""


@sshkey_cli.command(name="list")
def _list() -> None:
    """キーペア一覧."""
    pprint(find_all())  # noqa: T203


@sshkey_cli.command()
def create() -> None:
    """秘密鍵生成."""
    kp = create_keypair()
    kp.write()
    msg = f"{kp.name}の公開鍵を登録し、秘密鍵をファイル出力しました"
    click.echo(msg)


@sshkey_cli.command()
def remove() -> None:
    """登録済み公開鍵削除."""
    body = click.get_text_stream("stdin").read()
    click.echo("###############")
    click.echo(body)
