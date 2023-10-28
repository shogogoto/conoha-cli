"""snapshot cli."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features._shared.view.domain import view_options
from conoha_client.snapshot.repo import list_snapshots

if TYPE_CHECKING:
    from conoha_client.features.image.domain.image import Image


@click.group("snapshot")
def snapshot_cli() -> None:
    """Snapshot cli group."""


@snapshot_cli.command("ls")
@view_options
def list_() -> list[Image]:
    """スナップショット一覧."""
    return list_snapshots().root


@snapshot_cli.command()
def save() -> None:
    """スナップショットを名前をつけて保存."""


@snapshot_cli.command()
def restore() -> None:
    """スナップショットからVM起動."""


@snapshot_cli.command("rm")
def remove() -> None:
    """スナップショットを削除."""
