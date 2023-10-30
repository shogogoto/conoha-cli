"""snapshot cli."""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

import click

from conoha_client.features._shared import (
    add_vm_options,
    view_options,
)
from conoha_client.features.plan.domain import Memory

from .repo import (
    list_snapshots,
    remove_snapshot,
    restore_snapshot,
    save_snapshot,
)

if TYPE_CHECKING:
    from conoha_client.features.image.domain.image import Image


@click.group("snapshot")
def snapshot_cli() -> None:
    """スナップショット=ユーザーがVMから作成したイメージ."""


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
    overridden = save_snapshot(vm_id, name)
    if overridden:
        click.echo("old snapshot was deleted.")
    click.echo(f"{vm_id} was snapshot as {name}.")


@snapshot_cli.command(name="restore", help="スナップショットからVM起動")
@click.argument("image_id", nargs=1, type=click.UUID)
@click.argument("memory", nargs=1, type=click.Choice(Memory))
@add_vm_options
def restore(
    admin_password: str,
    keypair_name: str,
    image_id: UUID,
    memory: Memory,
) -> None:
    """スナップショットからVM起動."""
    added, img = restore_snapshot(
        image_id,
        memory,
        admin_password,
        keypair_name,
    )
    click.echo(f"VM(uuid={added.vm_id}) was restored from {img.name} snapshot")


@snapshot_cli.command("rm")
@click.argument("image_id", nargs=1, type=click.UUID)
def remove(image_id: UUID) -> None:
    """スナップショットを削除."""
    img = remove_snapshot(image_id)
    click.echo(f"{img.name} snapshot was deleted.")
