"""おためしCLI."""

import click
from click_shell import shell

from conoha_client.features import list_vm_cli, sshkey_cli
from conoha_client.features.billing.cli import billing_cli
from conoha_client.features.image.cli import vm_image_cli
from conoha_client.features.plan.cli import vm_plan_cli


# @click.group()
@shell(prompt="(conoha-client) ")
def cli() -> None:
    """root."""


@click.group(name="vm")
def vm_cli() -> None:
    """VM関連."""


def main() -> None:
    """CLI設定用."""
    vm_cli.add_command(vm_plan_cli)
    vm_cli.add_command(vm_image_cli)
    vm_cli.add_command(list_vm_cli)
    cli.add_command(vm_cli)
    cli.add_command(sshkey_cli)
    cli.add_command(billing_cli)
    cli()
