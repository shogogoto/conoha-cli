"""snapshot cli."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client._shared.renforced_vm.query import find_reinforced_vm_by_id
from conoha_client.features._shared import (
    add_vm_options,
    view_options,
)
from conoha_client.features._shared.command_option import each_args
from conoha_client.features.image.repo import remove_image
from conoha_client.features.plan.domain import Memory
from conoha_client.features.template.domain import template_io
from conoha_client.features.vm.repo.query import complete_vm

from .repo import (
    complete_snapshot,
    list_snapshots,
    restore_snapshot,
    save_snapshot,
)

if TYPE_CHECKING:
    from conoha_client._shared.renforced_vm.domain import ReinforcedVM
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
@click.argument("vm_id", nargs=1, type=click.STRING)
@click.argument("name", nargs=1, type=click.STRING)
def save(vm_id: str, name: str) -> None:
    """VMをイメージとして保存."""
    vm = complete_vm(vm_id)
    overridden = save_snapshot(vm.vm_id, name)
    if overridden:
        click.echo("old snapshot was deleted.")
    click.echo(f"{vm.vm_id} was snapshot as {name}.")


@snapshot_cli.command(name="restore", help="スナップショットからVM起動")
@click.argument("image_id", nargs=1, type=click.STRING)
@click.argument("memory", nargs=1, type=click.Choice(Memory))
@template_io
@add_vm_options
def restore(
    admin_password: str,
    keypair_name: str,
    image_id: str,
    memory: Memory,
) -> ReinforcedVM:
    """スナップショットからVM起動."""
    added, img = restore_snapshot(
        image_id,
        memory,
        admin_password,
        keypair_name,
    )
    click.echo(f"VM(uuid={added.vm_id}) was restored from {img.name} snapshot")
    return find_reinforced_vm_by_id(added.vm_id)


@snapshot_cli.command("rm")
@each_args("image_ids", converter=complete_snapshot)
def remove(image: Image) -> None:
    """スナップショットを削除."""
    remove_image(image)
    click.echo(f"{image.name} snapshot was deleted.")
