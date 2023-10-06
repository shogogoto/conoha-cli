"""Usecase."""
from __future__ import annotations

import os
from typing import TYPE_CHECKING

import click

from conoha_client.add_vm.repo import AddVMCommand, ImageInfoRepo, find_plan_id

if TYPE_CHECKING:
    from conoha_client.add_vm.domain.added_vm import AddedVM
    from conoha_client.add_vm.domain.domain import Application, OSVersion


def get_password() -> str:
    """VMのrootパスワードをprompt or 環境変数から取得する."""
    if "OS_ADMIN_PASSWORD" in os.environ:
        return os.environ["OS_ADMIN_PASSWORD"]
    msg = "VMのroot userのパスワードを入力してくだいさい"
    return click.prompt(msg, hide_input=True, confirmation_prompt=True)


def get_sshkey_name() -> str | None:
    """VMのsshkeyペア名をprompt or 環境変数から取得する."""
    if "OS_SSHKEY_NAME" in os.environ:
        return os.environ["OS_SSHKEY_NAME"]
    msg = "VMに紐付けるsshkey名を入力してくだいさい"
    return click.prompt(msg, hide_input=True, confirmation_prompt=True)


def add_vm(
    repo: ImageInfoRepo,
    os_version: OSVersion,
    app: Application,
) -> AddedVM:
    """Add VM Usecase."""
    flavor_id = find_plan_id(repo.memory)
    image_id = repo.find_image_id(os_version, app)

    cmd = AddVMCommand(
        flavor_id=flavor_id,
        image_id=image_id,
        admin_pass=get_password(),
        sshkey_name=get_sshkey_name(),
    )
    return cmd()
