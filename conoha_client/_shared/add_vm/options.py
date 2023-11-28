from __future__ import annotations

import functools
from typing import Callable, Concatenate, ParamSpec, TypeAlias, TypeVar

import click

from conoha_client.features.image.domain.distribution import (
    Application,
    Distribution,
    DistVersion,
)

P = ParamSpec("P")
T = TypeVar("T")

Wrapped: TypeAlias = Callable[
    Concatenate[
        Distribution,
        DistVersion,
        Application,
        P,
    ],
    T,
]


def identify_prior_image_options(func: Wrapped) -> Wrapped:
    """Add VM共通オプション."""

    @click.option(
        "--dist",
        "-d",
        type=click.Choice(Distribution),
        default=Distribution.UBUNTU,
        show_default=True,
    )
    @click.option(
        "--version",
        "-v",
        default="latest",
        help="latestの場合最新バージョンが指定される",
        show_default=True,
        type=DistVersion.parse,
    )
    @click.option(
        "--app",
        "-a",
        default="null",
        help="アプリ名.NONEは指定なし",
        show_default=True,
        type=Application.parse,
    )
    @functools.wraps(func)
    def wrapper(
        dist: Distribution,
        version: DistVersion,
        app: Application,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        return func(
            *args,
            dist=dist,
            version=version,
            app=app,
            **kwargs,
        )

    return wrapper
