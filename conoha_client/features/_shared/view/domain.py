"""CLI表示用モデル変換."""
from __future__ import annotations

import functools
import json
from typing import Callable, Literal, ParamSpec, TypeVar

import click
from pydantic import BaseModel
from tabulate import tabulate


class ExtraKeyError(Exception):
    """View表示keysにモデルプロパィにない値が指定された."""


R = TypeVar("R", bound=BaseModel)


def model_filter(model: R, keys: set[str] | None = None) -> dict:
    """モデルから特定のプロパティのみのjsonへ変換.

    :param model: (BaseModel)ドメインモデル
    :param keys: 抽出したいプロパティ名のリスト
    :return: JSONable object
    """
    all_keys = model.model_fields_set
    if keys is None:
        keys = all_keys
    extra = keys - all_keys
    if len(extra) > 0:
        msg = (
            f"{extra}は{model.__class__}に含まれていないキーです."
            f"{all_keys}に含まれるキーのみを入力してください"
        )
        raise ExtraKeyError(msg)
    return model.model_dump(mode="json", include=keys)


Style = Literal["json", "table"]


def view(
    models: list[R],
    keys: set[str] | None,
    style: Style = "table",
) -> None:
    """Print models.

    :param models: domain model list
    :param keys: property names for filter
    :param style: print style: json or table
    """
    js = [model_filter(m, keys) for m in models]
    if style == "json":
        txt = json.dumps(js, indent=2)
    elif style == "table":
        txt = tabulate(js, headers="keys", showindex=True)
    click.echo(txt)


P = ParamSpec("P")


def view_options(func: Callable[P, list[R]]) -> Callable[P, None]:
    """一覧表示系の共通オプション.

    参考: https://qiita.com/ainamori/items/5e68ec8dde4a46da104d
    """

    @click.option("--style", type=click.Choice(["table", "json"]), default="table")
    @click.argument("keys", nargs=-1)
    @functools.wraps(func)
    def wrapper(
        keys: set[str],
        style: Style,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        models = func(*args, **kwargs)
        _keys = set(keys) if len(keys) > 0 else None
        view(models, _keys, style)

    return wrapper
