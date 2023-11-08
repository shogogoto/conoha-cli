"""VM操作CLI."""
from __future__ import annotations

from uuid import UUID

import click

from conoha_client.features._shared.command_option import each_args
from conoha_client.features.vm.repo.query import complete_vm_id

from .repo import VMActionCommands, remove_vm


@click.group()
def vm_actions_cli() -> None:
    """VM操作関連."""


@vm_actions_cli.command(name="rm", help="VM削除")
@each_args("vm_ids", converter=complete_vm_id)
def remove_cli(vm_id: UUID) -> None:
    """VM削除."""
    remove_vm(vm_id)
    click.echo(f"{vm_id} was removed.")


@vm_actions_cli.command(name="stop", help="VMシャットダウン")
@each_args("vm_ids", converter=complete_vm_id)
def shutdown_cli(vm_id: UUID) -> None:
    """VMシャットダウン."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.shutdown()
    click.echo(f"{vm_id} was shutdowned.")


@vm_actions_cli.command(name="boot", help="VM起動")
@each_args("vm_ids", converter=complete_vm_id)
def boot_cli(vm_id: UUID) -> None:
    """VM起動."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.boot()
    click.echo(f"{vm_id} was booted.")


@vm_actions_cli.command(name="reboot", help="VM再起動")
@each_args("vm_ids", converter=complete_vm_id)
def reboot_cli(vm_id: UUID) -> None:
    """VM再起動."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.reboot()
    click.echo(f"{vm_id} was rebooted.")
