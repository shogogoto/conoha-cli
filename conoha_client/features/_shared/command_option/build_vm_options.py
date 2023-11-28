from __future__ import annotations

import functools
from typing import Callable, Concatenate, ParamSpec, TypeVar

import click

from conoha_client.features._shared.prompt import pw_prompt, sshkey_prompt

P = ParamSpec("P")
T = TypeVar("T")

Wrapped = Callable[Concatenate[str, str, P], T]


def build_vm_options_factory(pw_envvar: str, kw_envvar: str) -> Callable:
    def f(func: Wrapped) -> Wrapped:
        """Add VM共通オプション."""

        @click.option(
            "--admin-password",
            "-pw",
            envvar=pw_envvar,
            show_envvar=True,
            help="VMのrootユーザーのパスワード",
        )
        @click.option(
            "--keypair-name",
            "-k",
            envvar=kw_envvar,
            show_envvar=True,
            help="sshkeyのペア名",
            show_default=True,
        )
        @functools.wraps(func)
        def wrapper(
            admin_password: str | None,
            keypair_name: str | None,
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:
            return func(
                *args,
                admin_password=admin_password or pw_prompt(),
                keypair_name=keypair_name or sshkey_prompt(),
                **kwargs,
            )

        return wrapper

    return f


build_vm_options = build_vm_options_factory(
    "OS_ADMIN_PASSWORD",
    "OS_SSHKEY_NAME",
)
