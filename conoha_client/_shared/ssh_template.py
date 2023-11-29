import functools
import os
from typing import Any, Callable, ParamSpec

import click

from conoha_client.features._shared.command_option.build_vm_options import (
    build_vm_options_factory,
)
from conoha_client.features._shared.command_option.default_callback import ClickCallback
from conoha_client.features.template.domain import template_io_factory

P = ParamSpec("P")


def create_env_callback(envvar: str) -> ClickCallback:
    def _callback(
        ctx: click.Context,
        param: click.Parameter,  # noqa: ARG001
        value: Any,  # noqa: ANN401
    ) -> Any:  # noqa: ANN401
        envs_suffix = ctx.params["envs_suffix"]
        if envs_suffix != "":
            click.echo(f"envvar redirect to {envvar}{envs_suffix}")
        ret = os.environ[f"{envvar}{envs_suffix}"]
        return value.__class__(ret)

    return _callback


def ssh_template_options(f: Callable[P, Any]) -> Callable:
    @click.option(
        "--envs-suffix",
        "-E",
        required=True,
        default="",
        show_default=True,
        type=click.STRING,
        help="VM設定",
        is_eager=True,
    )
    @template_io_factory(
        "OS_TEMPLATE_READ",
        "OS_TEMPLATE_WRITE",
        r_callback=create_env_callback("OS_TEMPLATE_READ"),
        w_callback=create_env_callback("OS_TEMPLATE_WRITE"),
    )
    @build_vm_options_factory(
        "OS_ADMIN_PASSWORD",
        "OS_SSHKEY_NAME",
        pw_callback=create_env_callback("OS_ADMIN_PASSWORD"),
        kw_callback=create_env_callback("OS_SSHKEY_NAME"),
    )
    @functools.wraps(f)
    def wrapper(
        envs_suffix: str,  # noqa: ARG001
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Any:  # noqa: ANN401
        return f(*args, **kwargs)

    return wrapper
