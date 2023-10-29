"""snapshot cli."""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

import click

from conoha_client.features._shared import (
    add_vm_options,
    pw_prompt,
    sshkey_prompt,
    view_options,
)
from conoha_client.features.image.repo import (
    remove_snapshot,
)
from conoha_client.features.plan.domain import Memory
from conoha_client.features.plan.repo import find_vmplan
from conoha_client.features.vm.repo.command import AddVMCommand
from conoha_client.snapshot.repo import list_snapshots, save_snapshot

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
    save_snapshot(vm_id, name)
    click.echo(f"{vm_id} was snapshot as {name}.")


@snapshot_cli.command(name="restore", help="スナップショットからVM起動")
@click.argument("image_id", nargs=1, type=click.UUID)
@click.argument("memory", nargs=1, type=click.Choice(Memory))
@add_vm_options
def restore(
    admin_password: str | None,
    keypair_name: str | None,
    image_id: UUID,
    memory: Memory,
) -> None:
    """スナップショットからVM起動."""
    img = list_snapshots.find_by_id(image_id)
    cmd = AddVMCommand(
        flavor_id=find_vmplan(memory).flavor_id,
        image_id=img.image_id,
        admin_pass=admin_password or pw_prompt(),
    )
    added = cmd(keypair_name or sshkey_prompt())
    click.echo(f"VM(uuid={added.vm_id}) was restored from {img.name} snapshot")


@snapshot_cli.command("rm")
@click.argument("image_id", nargs=1, type=click.UUID)
def remove(image_id: UUID) -> None:
    """スナップショットを削除."""
    img = list_snapshots.find_by_id(image_id)
    remove_snapshot(img)
    click.echo(f"{img.name} snapshot was deleted.")
