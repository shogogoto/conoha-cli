"""add VM CLI."""

import click

from .domain import Memory
from .repo import add_vm


@click.command("add")
@click.argument("memory", type=Memory)
def add_vm_cli(memory: Memory) -> None:
    """Add VM CLI."""
    click.echo(memory.expression)
    add_vm(memory)
