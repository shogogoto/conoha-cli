"""snapshot cli."""
from __future__ import annotations

import os
from typing import TYPE_CHECKING
from uuid import UUID

import click

from conoha_client.features._shared.prompt import pw_prompt, sshkey_prompt
from conoha_client.features._shared.view.domain import view_options
from conoha_client.features.image.repo import (
    remove_snapshot,
)
from conoha_client.features.plan.domain import Memory
from conoha_client.features.plan.repo import find_vmplan
from conoha_client.features.vm.repo.command import AddVMCommand
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
@view_options
@click.argument("image_id", nargs=1, type=click.UUID)
@click.argument("memory", nargs=1, type=click.Choice(Memory))
@click.option(
    "--admin-password",
    "-pw",
    default=lambda: os.getenv("OS_ADMIN_PASSWORD", None),
    help="VMのrootユーザーのパスワード:OS_ADMIN_PASSWORD環境変数の値が設定される",
    show_default=True,
)
@click.option(
    "--keypair-name",
    "-k",
    default=lambda: os.getenv("OS_SSHKEY_NAME", None),
    help="sshkeyのペア名:OS_SSHKEY_NAME環境変数の値が設定される",
    show_default=True,
)
def restore(
    image_id: UUID,
    memory: Memory,
    admin_password: str | None,
    keypair_name: str | None,
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
