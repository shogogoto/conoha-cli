"""snapshot cli."""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

import click

from conoha_client.features._shared.view.domain import view_options
from conoha_client.features.image.repo import (
    list_images,
    remove_snapshot,
)
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


# @snapshot_cli.command()
# @view_options
# @click.argument("name", nargs=1, type=click.STRING)
# def restore(name: str) -> list[Image]:
#     """スナップショットからVM起動."""
#     # img = find_image_by_starts_with(name, "name")
#     # print(img)
#     # return [img]


@snapshot_cli.command("rm")
@click.argument("image_id", nargs=1, type=click.UUID)
def remove(image_id: UUID) -> None:
    """スナップショットを削除."""
    img = list_images().find_by_id(image_id)
    remove_snapshot(img)
    click.echo(f"{img.name} snapshot was deleted.")
