from __future__ import annotations

import os
from typing import Callable, Concatenate, ParamSpec, TypeVar

import click

from conoha_client.features._shared.prompt import pw_prompt, sshkey_prompt

P = ParamSpec("P")
T = TypeVar("T")


def add_vm_options(
    func: Callable[Concatenate[str, str, P], T],
) -> Callable[Concatenate[str, str, P], T]:
    """Add VM共通オプション."""

    @click.option(
        "--admin-password",
        "-pw",
        default=lambda: os.getenv("OS_ADMIN_PASSWORD", None),
        help="VMのrootユーザーのパスワード:OS_ADMIN_PASSWORD環境変数の値が設定される",
        show_default=True,
    )
    @click.option(
        "--keypair-name",
        "-k",
        default=lambda: os.getenv("OS_SSHKEY_NAME", None),
        help="sshkeyのペア名:OS_SSHKEY_NAME環境変数の値が設定される",
        show_default=True,
    )
    def wrapper(
        admin_password: str | None,
        keypair_name: str | None,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        return func(
            admin_password or pw_prompt(),
            keypair_name or sshkey_prompt(),
            *args,
            **kwargs,
        )

    return wrapper
