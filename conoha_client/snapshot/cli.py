"""snapshot cli."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client._shared import save_snapshot
from conoha_client._shared.renforced_vm.query import find_reinforced_vm_by_id
from conoha_client._shared.ssh_template import ssh_template_options
from conoha_client.features._shared import (
    view_options,
)
from conoha_client.features._shared.command_option import each_args
from conoha_client.features.image.repo import remove_image
from conoha_client.features.plan.domain import Memory
from conoha_client.features.vm.repo.query import complete_vm
from conoha_client.features.vm_actions.repo import VMActionCommands

from .repo import (
    complete_snapshot_by_name,
    list_snapshots,
    restore_snapshot,
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
    old_id = save_snapshot(vm.vm_id, name)
    if old_id is not None:
        click.echo(f"old snapshot({old_id}) was deleted.")
    click.echo(f"{vm.vm_id} was snapshot as {name}.")


@snapshot_cli.command(name="restore", help="スナップショットからVM起動")
@click.argument("name", nargs=1, type=click.STRING)
@click.argument("memory", nargs=1, type=click.Choice(Memory))
@ssh_template_options
def restore(
    admin_password: str,
    keypair_name: str,
    name: str,
    memory: Memory,
) -> ReinforcedVM:
    """スナップショットからVM起動."""
    added, img = restore_snapshot(
        name,
        memory,
        admin_password,
        keypair_name,
    )
    vm = find_reinforced_vm_by_id(added.vm_id)
    click.echo(f"VM(uuid={added.vm_id}) was restored from {img.name} snapshot")
    return vm


@snapshot_cli.command(name="rebuild", help="スナップショットからVMを再構築")
@click.argument("vm_id", nargs=1, type=click.STRING)
@click.argument("name", nargs=1, type=click.STRING)
@ssh_template_options
def rebuild(
    admin_password: str,
    keypair_name: str,
    vm_id: str,
    name: str,
) -> ReinforcedVM:
    """スナップショットからVM起動."""
    vm = complete_vm(vm_id)
    img = complete_snapshot_by_name(name)
    cmd = VMActionCommands(vm_id=vm.vm_id)
    cmd.rebuild(
        image_id=img.image_id,
        admin_pass=admin_password,
        sshkey_name=keypair_name,
    )
    vm = find_reinforced_vm_by_id(vm.vm_id)
    click.echo(f"VM(uuid={vm.vm_id}) was rebuild from {img.name} snapshot")
    return vm


@snapshot_cli.command("rm")
@each_args("names", converter=complete_snapshot_by_name)
def remove(snapshot: Image) -> None:
    """スナップショットを削除."""
    remove_image(snapshot)
    click.echo(f"{snapshot.name} snapshot was deleted.")
