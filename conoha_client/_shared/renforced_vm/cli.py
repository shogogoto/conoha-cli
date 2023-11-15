from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client._shared.renforced_vm.query import list_reinforced_vms
from conoha_client.features._shared.view.domain import view_options
from conoha_client.features.vm.repo.query import list_vms

if TYPE_CHECKING:
    from conoha_client._shared.renforced_vm.domain import ReinforcedVM

_help = "list VM as human friendly"


@click.command(name="lsvm", help=_help)
@view_options
def reinforced_vm_cli() -> list[ReinforcedVM]:
    return list_reinforced_vms()


@click.command(name="ls")
@click.option("--reinforce", "-r", is_flag=True, help=_help)
@view_options
def list_vm_cli(reinforce: bool) -> list:
    """契約中サーバー一覧取得コマンド."""
    if reinforce:
        return list_reinforced_vms()
    return list_vms()


@click.command(name="ls", help=_help)
@view_options
def shortcut_vm_cli() -> list[ReinforcedVM]:
    return list_reinforced_vms()
