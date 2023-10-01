"""add VM CLI."""
from __future__ import annotations

import click

from conoha_client.add_vm.repo import (
    find_available_os_latest_version,
    list_available_os_versions,
    list_image_names,
)
from conoha_client.features._shared.view.domain import view_options

from .domain import OS, Memory, Version


@click.group("add", invoke_without_command=True)
@click.option("--memory", "-m", type=click.Choice(Memory))
@click.option("--os", "-o", type=click.Choice(OS), default=OS.UBUNTU)
@click.option("--os-version", "-ov", default="latest")
# @click.option("--app", "-a", default="")
# @click.option("--app-version", "-av", default="")
@click.pass_context
def add_vm_cli(
    ctx: click.Context,
    memory: Memory,
    os: OS,
    os_version: Version,
    # app: str,
    # app_version: Version,
) -> None:
    """Add VM CLI."""
    ctx.ensure_object(dict)
    ctx.obj["memory"] = memory
    ctx.obj["os"] = os
    ctx.obj["os_version"] = Version(value=os_version)
    # ctx.obj["app"] = app
    # ctx.obj["app_version"] = app_version
    # add_vm(memory, os, app)
    # print(memory.expression, memory.is_smallest(), os, app)
    # add_vm(memory)


@add_vm_cli.command(name="os-vers")
@view_options
@click.pass_obj
def list_os_versions(obj: object) -> list[Version]:
    """利用可能なOSバージョンを検索する."""
    return list_available_os_versions(
        memory=obj["memory"],
        os=obj["os"],
        image_names=list_image_names,
    )


@add_vm_cli.command(name="os-latest")
@view_options
@click.pass_obj
def find_latest_os_version(obj: object) -> list[Version]:
    """利用可能な最新のOSバージョンを検索する."""
    v = find_available_os_latest_version(
        memory=obj["memory"],
        os=obj["os"],
        image_names=list_image_names,
    )
    return [v]


# @add_vm_cli.command(name="apps")
# @click.pass_obj
# def list_apps(obj: object) -> list[Version]:
#     """利用可能なアプリケーションを検索する."""
#     a = list_available_apps(
#         memory=obj["memory"],
#         os=obj["os"],
#         os_version=obj["os_version"],
#     )
#     print(a)


# addコマンドを実行する流れ
# 1. memoryを選択する osやapp選択に先行させないと利用可能なos,appが確定しない
# 2. 利用可能なimageを検索する

#    os選択
#    利用可能バージョン選択
#    利用可能アプリ選択
#    アプリバージョン選択
# 3. パスワード設定
# 4. ssh-key設定
# 5. server名設定 ssh configに使う

# VM起動
# VMのipアドレスを取得
# ssh configファイルが出力される
