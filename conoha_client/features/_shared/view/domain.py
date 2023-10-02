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


def check_include_keys(model: R, keys: set[str]) -> None:
    """キーがmodelに含まれていなければエラー."""
    all_keys = set(model.__class__.model_fields)
    if keys is None:
        keys = all_keys
    extra = keys - all_keys
    if len(extra) > 0:
        msg = (
            f"{extra}は{model.__class__}に含まれていないキーです."
            f"{all_keys}に含まれるキーのみを入力してください"
        )
        raise ExtraKeyError(msg)


def model_filter(model: R, keys: set[str] | None = None) -> dict:
    """モデルから特定のプロパティのみのjsonへ変換.

    :param model: (BaseModel)ドメインモデル
    :param keys: 抽出したいプロパティ名のリスト
    :return: JSONable object
    """
    check_include_keys(model, keys)
    return model.model_dump(mode="json", include=keys)


def _tabulate(js: list[dict], pass_command: bool) -> str:
    """jsonリストをテーブル形式文字列へ変換.

    :param js: jsoable list
    :param pass_command: disable decoration of table view for passing stdout by pipeline
    """
    if pass_command:
        return tabulate(js, headers=(), tablefmt="plain", showindex=False)
    return tabulate(js, headers="keys", showindex=True)


def view(
    models: list[R],
    keys: set[str],
    style: Style,
    pass_command: bool,
) -> None:
    _keys = set(keys) if len(keys) > 0 else None
    js = [model_filter(m, _keys) for m in models]

    if style == "json":
        txt = json.dumps(js, indent=2)
    elif style == "table":
        txt = _tabulate(js, pass_command)
    click.echo(txt)


Style = Literal["json", "table"]


P = ParamSpec("P")


def view_options(func: Callable[P, list[R]]) -> Callable[P, None]:
    """一覧表示系の共通オプション.

    参考: https://qiita.com/ainamori/items/5e68ec8dde4a46da104d
    """

    @click.argument("keys", nargs=-1, default=None)
    @click.option(
        "--style",
        "-s",
        type=click.Choice(["table", "json"]),
        default="table",
        help="print style",
    )
    @click.option(
        "--pass-command",
        "-p",
        is_flag=True,
        default=False,
        help="他のコマンドに渡しやすいようにtable viewの装飾をなくす",
    )
    @functools.wraps(func)
    def wrapper(
        keys: set[str],
        style: Style,
        pass_command: bool,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        models = func(*args, **kwargs)
        view(models, keys, style, pass_command)

    return wrapper
