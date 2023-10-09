"""VM操作CLI."""
from __future__ import annotations

from typing import TextIO
from uuid import UUID

import click

from conoha_client.features.vm_actions.repo import remove_vm


@click.group()
def vm_actions_cli() -> None:
    """VM操作関連."""


@vm_actions_cli.command(name="rm")
@click.argument("vm_ids", nargs=-1, type=click.UUID)
@click.option(
    "--file",
    "-f",
    type=click.File("r"),
    default="-",
    help="削除対象のUUIDをファイルから読み取る(default:標準入力)",
)
def remove(
    vm_ids: tuple[UUID],
    file: TextIO,
) -> None:
    """VM削除."""
    click.echo("remove vm")
    vm_ids = list(vm_ids)
    if not file.isatty():
        lines = file.read().splitlines()
        uids = [UUID(line) for line in lines]
        vm_ids.extend(uids)
    for vm_id in vm_ids:
        remove_vm(vm_id)
