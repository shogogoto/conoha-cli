"""VM resize cli."""

import click

from conoha_client.features.plan.domain import Memory
from conoha_client.features.plan.repo import find_vmplan
from conoha_client.features.vm.repo.query import complete_vm
from conoha_client.features.vm_actions.repo import VMActionCommands


@click.command(name="resize")
@click.argument("vm_id", nargs=1, type=click.STRING)
@click.argument("memory", nargs=1, type=click.Choice(Memory))
def resize_cli(vm_id: str, memory: Memory) -> None:
    """VMのメモリサイズを変更."""
    vm = complete_vm(vm_id)
    cmd = VMActionCommands(vm_id=vm.vm_id)
    cmd.resize(find_vmplan(memory).flavor_id)
