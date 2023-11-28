"""VM resize cli."""

from uuid import UUID

import click

from conoha_client.features._shared.command_option import each_args
from conoha_client.features.plan.domain import Memory
from conoha_client.features.plan.repo import find_vmplan
from conoha_client.features.vm.repo.query import complete_vm, complete_vm_id
from conoha_client.features.vm_actions.repo import VMActionCommands


@click.group("resize")
def vm_resize_cli() -> None:
    """VMのメモリプランを変更する."""


@vm_resize_cli.command(name="resize")
@click.argument("vm_id", nargs=1, type=click.STRING)
@click.argument("memory", nargs=1, type=click.Choice(Memory))
def resize(vm_id: str, memory: Memory) -> None:
    """VMのメモリサイズを変更."""
    vm = complete_vm(vm_id)
    cmd = VMActionCommands(vm_id=vm.vm_id)
    cmd.resize(find_vmplan(memory).flavor_id)
    click.echo(f"{vm.vm_id} is resizing")


@vm_resize_cli.command(name="resize-confirm")
@each_args("vm_ids", converter=complete_vm_id)
def confirm(vm_id: UUID) -> None:
    """VMののリサイズ確定."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.confirm_resize()
    click.echo(f"{vm_id} was resized")


@vm_resize_cli.command(name="resize-revert")
@each_args("vm_ids", converter=complete_vm_id)
def revert(vm_id: UUID) -> None:
    """VMののリサイズ取り消し."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.revert_resize()
    click.echo(f"{vm_id} reverted to previous size")
