"""add VM CLI."""
from __future__ import annotations

from operator import attrgetter
from typing import TYPE_CHECKING

import click

from conoha_client._shared.renforced_vm.query import find_reinforced_vm_by_id
from conoha_client.add_vm.repo import DistQuery, add_vm_command
from conoha_client.features._shared.command_option import add_vm_options
from conoha_client.features._shared.view.domain import view_options
from conoha_client.features.image.domain import (
    Application,
    Distribution,
    DistVersion,
)
from conoha_client.features.plan.domain import Memory
from conoha_client.features.template.domain import template_io

if TYPE_CHECKING:
    from conoha_client._shared.renforced_vm.domain import ReinforcedVM


@click.group("add", invoke_without_command=True, help="VM新規追加")
@click.option(
    "--memory",
    "-m",
    type=click.Choice(Memory),
    required=True,
    help="VMのRAM容量[GB]",
)
@click.option(
    "--dist",
    "-d",
    type=click.Choice(Distribution),
    default=Distribution.UBUNTU,
    show_default=True,
)
@click.option(
    "--version",
    "-v",
    default="latest",
    help="latestの場合最新バージョンが指定される",
    show_default=True,
    type=DistVersion.parse,
)
@click.option(
    "--app",
    "-a",
    default="null",
    help="アプリ名.NONEは指定なし",
    show_default=True,
    type=Application.parse,
)
@template_io
@add_vm_options
@click.pass_context
def add_vm_cli(  # noqa: PLR0913
    ctx: click.Context,
    admin_password: str,
    keypair_name: str,
    memory: Memory,
    dist: Distribution,
    version: DistVersion,
    app: Application,
) -> ReinforcedVM | None:
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
        vm = find_reinforced_vm_by_id(added.vm_id)
        click.echo(f"VM(uuid={vm.vm_id}) was added newly")
        return vm
    return None


@add_vm_cli.command(name="vers")
@view_options
@click.pass_obj
def list_os_versions(obj: object) -> list[DistVersion]:
    """利用可能なOSバージョンを検索する."""
    vers = obj["q"].available_vers()
    return sorted(vers, key=attrgetter("value"))


@add_vm_cli.command(name="apps")
@view_options
@click.pass_obj
def find_apps(obj: object) -> list[Application]:
    """利用可能なアプリケーションを検索する."""
    v = obj["version"]
    apps = obj["q"].apps(v)
    return sorted(apps, key=attrgetter("value"))
