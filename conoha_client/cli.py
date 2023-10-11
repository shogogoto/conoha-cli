"""おためしCLI."""

import click
from click_shell import shell

from conoha_client.features import (
    billing_cli,
    list_vm_cli,
    sshkey_cli,
    vm_actions_cli,
    vm_image_cli,
    vm_plan_cli,
)

from .add_vm import add_vm_cli


# @click.group()
@shell(prompt="(conoha-client) ")
def cli() -> None:
    """root."""


@click.group()
def vm_cli() -> None:
    """VM関連."""


def main() -> None:
    """CLI設定用."""
    vm_cli.add_command(list_vm_cli)
    vm_cli.add_command(add_vm_cli)
    vm_merged = click.CommandCollection(name="vm", sources=[vm_cli, vm_actions_cli])
    cli.add_command(vm_merged)
    cli.add_command(vm_plan_cli)
    cli.add_command(vm_image_cli)
    cli.add_command(sshkey_cli)
    cli.add_command(billing_cli)
    cli()
