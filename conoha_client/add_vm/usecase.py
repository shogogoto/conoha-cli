"""Usecase."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.add_vm.repo import (
    AddVMCommand,
    ImageInfoRepo,
    find_added,
    find_plan_id,
)

if TYPE_CHECKING:
    from conoha_client.add_vm.domain.domain import Application, OSVersion
    from conoha_client.features.list_vm.domain import Server


def get_password(value: str | None) -> str:
    """VMのrootパスワードをprompt or 環境変数から取得する."""
    if value is not None:
        return value
    msg = "VMのroot userのパスワードを入力してくだいさい"
    return click.prompt(msg, hide_input=True, confirmation_prompt=True)


def get_sshkey_name(value: str | None) -> str | None:
    """VMのsshkeyペア名をprompt or 環境変数から取得する."""
    if value is not None:
        return value
    msg = "VMに紐付けるsshkey名を入力してくだいさい"
    return click.prompt(msg, hide_input=True, confirmation_prompt=True)


def add_vm(
    repo: ImageInfoRepo,
    os_version: OSVersion,
    app: Application,
    admin_pass: str | None,
    sshkey_name: str | None = None,
) -> Server:
    """Add VM Usecase."""
    flavor_id = find_plan_id(repo.memory)
    image_id = repo.find_image_id(os_version, app)

    cmd = AddVMCommand(
        flavor_id=flavor_id,
        image_id=image_id,
        admin_pass=get_password(admin_pass),
    )
    added = cmd(get_sshkey_name(sshkey_name))
    return find_added(added.vm_id)
