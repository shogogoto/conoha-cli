"""snapshot cli."""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

import click

from conoha_client.features._shared.view.domain import view_options
from conoha_client.features.vm_actions.repo import VMActionCommands
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
@click.argument("vm_id", nargs=1, type=click.UUID)
@click.argument("name", nargs=1, type=click.STRING)
def save(vm_id: UUID, name: str) -> None:
    """VMをイメージとして保存."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.snapshot(name)
    click.echo(f"{vm_id} was snapshot as {name}.")


@snapshot_cli.command()
def restore() -> None:
    """スナップショットからVM起動."""


@snapshot_cli.command("rm")
def remove() -> None:
    """スナップショットを削除."""
