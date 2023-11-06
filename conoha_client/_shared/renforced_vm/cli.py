from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client._shared.renforced_vm.query import list_reinforced_vms
from conoha_client.features._shared.view.domain import view_options

if TYPE_CHECKING:
    from conoha_client._shared.renforced_vm.domain import ReinforcedVM


@click.command(name="lsvm", help="list VM as human friendly")
@view_options
def reinforced_vm_cli() -> list[ReinforcedVM]:
    return list_reinforced_vms()
