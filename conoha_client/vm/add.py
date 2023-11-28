"""add VM CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client._shared.add_vm.options import (
    add_subcommands,
    identify_prior_image_options,
)
from conoha_client._shared.add_vm.repo import DistQuery, add_vm_command
from conoha_client.features._shared.command_option import build_vm_options
from conoha_client.features.plan.domain import Memory
from conoha_client.features.template.domain import template_io

if TYPE_CHECKING:
    from conoha_client.features.image.domain import (
        Application,
        Distribution,
        DistVersion,
    )


@click.group("add", invoke_without_command=True, help="VM新規追加")
@click.option(
    "--memory",
    "-m",
    type=click.Choice(Memory),
    required=True,
    help="VMのRAM容量[GB]",
)
@identify_prior_image_options
@template_io
@build_vm_options
@click.pass_context
def vm_add_cli(  # noqa: PLR0913
    ctx: click.Context,
    admin_password: str,
    keypair_name: str,
    memory: Memory,
    dist: Distribution,
    version: DistVersion,
    app: Application,
) -> None:
    """Add VM CLI."""
    ctx.ensure_object(dict)
    query = DistQuery(memory=memory, dist=dist)
    ctx.obj["q"] = query
    ctx.obj["version"] = version
    ctx.obj["app"] = app
    if ctx.invoked_subcommand is None:
        cmd = add_vm_command(
            memory=memory,
            dist=dist,
            ver=version,
            app=app,
            admin_pass=admin_password,
        )
        added = cmd(keypair_name)
        click.echo(f"VM(uuid={added.vm_id}) was added newly")


add_subcommands(vm_add_cli)
