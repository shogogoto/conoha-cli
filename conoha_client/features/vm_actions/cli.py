"""VM操作CLI."""
from __future__ import annotations

from uuid import UUID

import click

from conoha_client.features.vm_actions.command_option import uuid_targets_options

from .repo import VMActionCommands, remove_vm


@click.group()
def vm_actions_cli() -> None:
    """VM操作関連."""


@vm_actions_cli.command(name="rm")
@uuid_targets_options
def remove_cli(vm_id: UUID) -> None:
    """VM削除."""
    remove_vm(vm_id)
    click.echo(f"{vm_id} was removed.")


@vm_actions_cli.command(name="shutdown")
@uuid_targets_options
def shutdown_cli(vm_id: UUID) -> None:
    """VMシャットダウン."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.shutdown()


@vm_actions_cli.command(name="boot")
@uuid_targets_options
def boot_cli(vm_id: UUID) -> None:
    """VM起動."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.boot()
    click.echo(f"{vm_id} was booted.")


@vm_actions_cli.command(name="reboot")
@uuid_targets_options
def reboot_cli(vm_id: UUID) -> None:
    """VM再起動."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.reboot()
    click.echo(f"{vm_id} was rebooted.")


@vm_actions_cli.command(name="snapshot")
@click.argument("vm_id", nargs=1, type=click.UUID)
@click.argument("name", nargs=1, type=click.STRING)
def snapshot_cli(vm_id: UUID, name: str) -> None:
    """VMをイメージとして保存."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.snapshot(name)
    click.echo(f"{vm_id} was snapshot.")
