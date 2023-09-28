"""CLI表示用モデル変換."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Callable, Literal, ParamSpec, TypeVar

import click
from tabulate import tabulate

if TYPE_CHECKING:
    from pydantic import BaseModel


class ExtraKeyError(Exception):
    """View表示keysにモデルプロパィにない値が指定された."""


def model_filter(model: BaseModel, keys: set[str] | None = None) -> dict:
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
        exkeys = ",".join(extra)
        msg = f"{exkeys}は{model.__class__}に含まれていないプロパティです"
        raise ExtraKeyError(msg)
    return model.model_dump(mode="json", include=keys)


def view(
    models: list[BaseModel],
    keys: set[str] | None,
    style: Literal["json", "table"] = "table",
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
R = TypeVar("R")


def list_options(func: Callable[P, R]) -> Callable[P, R]:
    """一覧表示系の共通オプション."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return wrapper
