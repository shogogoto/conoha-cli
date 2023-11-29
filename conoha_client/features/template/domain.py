"""template domain."""
from __future__ import annotations

import functools
from pathlib import Path
from typing import TYPE_CHECKING, Callable, ParamSpec, TypeAlias, TypeVar

import click
from pydantic import BaseModel

from conoha_client.features._shared.command_option import (
    default_callback,
)
from conoha_client.features.template.repo import TemplateRepo

if TYPE_CHECKING:
    from conoha_client.features._shared.command_option import (
        ClickCallback,
    )

P = ParamSpec("P")
T = TypeVar("T", bound=BaseModel)

Wrapped: TypeAlias = Callable[P, T | None]


def template_io_factory(
    r_envvar: str,
    w_envvar: str,
    r_callback: ClickCallback = default_callback,
    w_callback: ClickCallback = default_callback,
) -> Callable[[Wrapped], Callable]:
    """Create template io options."""

    def f(func: Wrapped) -> Callable:
        """Template cli options."""

        @click.option(
            "--read-template",
            "-r",
            "rpath",
            type=click.Path(
                dir_okay=False,
                readable=True,
                path_type=Path,
            ),
            envvar=r_envvar,
            show_envvar=True,
            help="テンプレートパス",
            callback=r_callback,
        )
        @click.option(
            "--write-template",
            "-w",
            "wpath",
            type=click.Path(
                dir_okay=False,
                writable=True,
                path_type=Path,
            ),
            envvar=w_envvar,
            show_envvar=True,
            help="書き出し先[default: OS_TEMPLATE_WRITE]",
            callback=w_callback,
        )
        @click.option(
            "--mapping",
            "-map",
            "mapping",
            nargs=2,
            multiple=True,
            type=click.Tuple([str, str]),
            default=[],
        )
        @functools.wraps(func)
        def wrapper(
            rpath: Path,
            wpath: Path,
            mapping: list[tuple[str, str]],
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T | None:
            model = func(*args, **kwargs)
            if model is None:
                return model
            if rpath is None:
                return model
            t = TemplateRepo[T](read_from=rpath, map_to=dict(mapping))
            if wpath is None:
                click.echo(t.apply(model))
            else:
                t.write(model, wpath)
            return model

        return wrapper

    return f


template_io = template_io_factory(
    r_envvar="OS_TEMPLATE_READ",
    w_envvar="OS_TEMPLATE_WRITE",
)
