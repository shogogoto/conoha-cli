"""VM rebuild CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client._shared.add_vm.options import (
    add_subcommands,
    identify_prior_image_options,
)
from conoha_client._shared.add_vm.repo import DistQuery
from conoha_client.features._shared.command_option import build_vm_options
from conoha_client.features.plan.repo import find_memory
from conoha_client.features.template.domain import template_io
from conoha_client.features.vm.repo.query import complete_vm
from conoha_client.features.vm_actions.repo import VMActionCommands

if TYPE_CHECKING:
    from conoha_client.features.image.domain.distribution import (
        Application,
        Distribution,
        DistVersion,
    )


@click.group(name="rebuild", invoke_without_command=True, help="VM再構築")
@click.option("--vm-id", "-i", type=click.STRING, required=True)
@identify_prior_image_options
@template_io
@build_vm_options
@click.pass_context
def vm_rebuild_cli(  # noqa: PLR0913
    ctx: click.Context,
    admin_password: str,
    keypair_name: str,
    vm_id: str,
    dist: Distribution,
    version: DistVersion,
    app: Application,
) -> None:
    """VM再起動."""
    ctx.ensure_object(dict)

    vm = complete_vm(vm_id)
    q = DistQuery(
        memory=find_memory(vm.flavor_id),
        dist=dist,
    )
    ctx.obj["q"] = q
    ctx.obj["version"] = version
    ctx.obj["app"] = app
    if ctx.invoked_subcommand is None:
        cmd = VMActionCommands(vm_id=vm.vm_id)
        cmd.rebuild(
            image_id=q.identify(version, app).image_id,
            admin_pass=admin_password,
            sshkey_name=keypair_name,
        )
        click.echo(f"{vm.vm_id} was rebuilt.")


add_subcommands(vm_rebuild_cli)