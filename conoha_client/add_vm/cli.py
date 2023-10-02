"""add VM CLI."""
from __future__ import annotations

import click

from conoha_client.add_vm.domain.domain import Application
from conoha_client.add_vm.repo import (
    find_available_os_latest_version,
    list_available_apps,
    list_available_os_versions,
    list_image_names,
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
    os_version: OSVersion,
    app: str,
    app_version: str,
) -> None:
    """Add VM CLI."""
    ctx.ensure_object(dict)
    ctx.obj["memory"] = memory
    ctx.obj["os"] = os
    ov = OSVersion(value=os_version, os=os)

    ctx.obj["os_version"] = ov
    _app = Application(name=app, version=app_version)
    ctx.obj["app"] = _app
    if ctx.invoked_subcommand is None:
        pass
        # find_image_id(memory, os, ov, _app)
        # print(image_id)
        # print(image_id)
        # print(image_id)


@add_vm_cli.command(name="os-vers")
@view_options
@click.pass_obj
def list_os_versions(obj: object) -> list[OSVersion]:
    """利用可能なOSバージョンを検索する."""
    return list_available_os_versions(
        memory=obj["memory"],
        os=obj["os"],
        image_names=list_image_names,
    )


@add_vm_cli.command(name="os-latest")
@view_options
@click.pass_obj
def find_latest_os_version(obj: object) -> list[OSVersion]:
    """利用可能な最新のOSバージョンを検索する."""
    v = find_available_os_latest_version(
        memory=obj["memory"],
        os=obj["os"],
        image_names=list_image_names,
    )
    return [v]


@add_vm_cli.command(name="apps")
@view_options
@click.pass_obj
def find_apps(obj: object) -> list[Application]:
    """利用可能なアプリケーションを検索する."""
    return list_available_apps(
        memory=obj["memory"],
        os=obj["os"],
        os_version=obj["os_version"],
        image_names=list_image_names,
    )
