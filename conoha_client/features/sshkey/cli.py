"""ssh鍵CLI."""


import click

from conoha_client.features._shared.view import view

from .repo import create_keypair, find_all


@click.group(name="sshkey")
def sshkey_cli() -> None:
    """キーペアCRUD."""


@sshkey_cli.command(name="ls")
def _list() -> None:
    """キーペア一覧."""
    view(find_all(), keys=None, style="json")
    view(find_all(), keys={"name"}, style="table")


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
