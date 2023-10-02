"""add VM CLI."""
from __future__ import annotations

import click

from conoha_client.add_vm.domain.domain import Application
from conoha_client.add_vm.repo import (
    ImageInfoRepo,
)
from conoha_client.features._shared.view.domain import view_options

from .domain import OS, Memory, OSVersion


@click.group("add", invoke_without_command=True)
@click.option("--memory", "-m", type=click.Choice(Memory), required=True)
@click.option("--os", "-o", type=click.Choice(OS), default=OS.UBUNTU, show_default=True)
@click.option(
    "--os-version",
    "-ov",
    default="latest",
    help="latestの場合最新バージョンが指定される",
    show_default=True,
)
@click.option(
    "--app",
    "-a",
    default="NONE",
    help="アプリ名.NONEは指定なし",
    show_default=True,
)
@click.option(
    "--app-version",
    "-av",
    default="NONE",
    help="アプリのバージョン.NONEは指定なし",
    show_default=True,
)
@click.pass_context
def add_vm_cli(  # noqa: PLR0913
    ctx: click.Context,
    memory: Memory,
    os: OS,
    os_version: str,
    app: str,
    app_version: str,
) -> None:
    """Add VM CLI."""
    ctx.ensure_object(dict)
    ctx.obj["repo"] = ImageInfoRepo(memory=memory, os=os)
    ctx.obj["os_version"] = OSVersion(value=os_version, os=os)
    ctx.obj["app"] = Application(name=app, version=app_version)
    if ctx.invoked_subcommand is None:
        pass


@add_vm_cli.command(name="os-vers")
@view_options
@click.pass_obj
def list_os_versions(obj: object) -> list[OSVersion]:
    """利用可能なOSバージョンを検索する."""
    return obj["repo"].available_os_versions


@add_vm_cli.command(name="os-latest")
@view_options
@click.pass_obj
def find_latest_os_version(obj: object) -> list[OSVersion]:
    """利用可能な最新のOSバージョンを検索する."""
    v = obj["repo"].available_os_latest_version
    return [v]


@add_vm_cli.command(name="apps")
@view_options
@click.pass_obj
def find_apps(obj: object) -> list[Application]:
    """利用可能なアプリケーションを検索する."""
    return obj["repo"].list_available_apps(obj["os_version"])
