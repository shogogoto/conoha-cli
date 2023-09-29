"""VM関連 CLI定義."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features._shared import view_options

from .repo import list_servers

if TYPE_CHECKING:
    from .domain import Server


@click.command(name="ls")
@view_options
def list_vm_cli() -> list[Server]:
    """契約中サーバー一覧取得コマンド."""
    return list_servers()
