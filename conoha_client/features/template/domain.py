"""template domain."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

import click
from pydantic import BaseModel

from conoha_client.features.template.repo import TemplateRepo

P = ParamSpec("P")
T = TypeVar("T", bound=BaseModel)


def template_io(func: Callable[P, T]) -> Callable:
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
        envvar="OS_TEMPLATE_READ",
        help="テンプレートパス",
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
        envvar="OS_TEMPLATE_write",
        help="書き出し先",
    )
    @click.option(
        "--mapping",
        "-m",
        nargs=2,
        multiple=True,
        type=click.Tuple([str, str]),
        default=None,
    )
    def wrapper(
        rpath: Path,
        wpath: Path,
        mapping: list[tuple[str, str]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        model = func(*args, **kwargs)
        if rpath is None:
            return model
        t = TemplateRepo[T](read_from=rpath, map_to=dict(mapping))
        if wpath is None:
            click.echo(t.apply(model))
        else:
            t.write(model, wpath)
        return model

    return wrapper
