"""おためしCLI."""

import click
from click_shell import shell

from conoha_client._shared.renforced_vm import list_vm_cli, reinforced_vm_cli
from conoha_client.features import (
    sshkey_cli,
    vm_actions_cli,
    vm_image_cli,
    vm_plan_cli,
)
from conoha_client.features.billing.cli import invoice_cli, order_cli, paid_cli
from conoha_client.resize import vm_resize_cli

from .add_vm import add_vm_cli
from .snapshot import snapshot_cli


# @click.group()
@shell(prompt="(conoha-client) ")
def cli() -> None:
    """root."""


@click.group()
def vm_cli() -> None:
    """VM関連."""


def main() -> None:
    """CLI設定用."""
    vm_cli.add_command(add_vm_cli)
    vm_merged = click.CommandCollection(
        name="vm",
        sources=[
            vm_cli,
            vm_actions_cli,
            vm_resize_cli,
        ],
        help="VM追加・削除など",
    )
    cli.add_command(vm_merged)
    cli.add_command(vm_plan_cli)
    cli.add_command(vm_image_cli)
    cli.add_command(sshkey_cli)

    cli.add_command(order_cli)
    cli.add_command(paid_cli)
    cli.add_command(invoice_cli)

    cli.add_command(snapshot_cli)
    cli.add_command(reinforced_vm_cli)
    vm_cli.add_command(list_vm_cli)
    cli()
