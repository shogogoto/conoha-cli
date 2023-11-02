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


def check_include_keys(t: type[R], keys: set[str]) -> None:
    """キーがmodelに含まれていなければエラー."""
    all_keys = set(t.model_fields)
    if keys is None:
        keys = all_keys
    extra = keys - all_keys
    if len(extra) > 0:
        msg = (
            f"{extra}は{t.__class__}に含まれていないキーです."
            f"{all_keys}に含まれるキーのみを入力してください"
        )
        raise ExtraKeyError(msg)


def model_extract(model: R, keys: set[str] | None = None) -> dict:
    """モデルから特定のプロパティのみのjsonへ変換.

    :param model: (BaseModel)ドメインモデル
    :param keys: 抽出したいプロパティ名のリスト
    :return: JSONable object
    """
    check_include_keys(model.__class__, keys)
    return model.model_dump(mode="json", include=keys)


def model_filter(models: list[R], key: str, value: str) -> list[R]:
    """modelをフィルターする."""

    def pred(e: R) -> bool:
        check_include_keys(e.__class__, {key})
        return value in str(getattr(e, key))

    return list(filter(pred, models))


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
    js = [model_extract(m, _keys) for m in models]

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

    @click.option(
        "--keys",
        "-k",
        multiple=True,
        default=None,
        help="表示キー[複数指定可]",
    )
    @click.option(
        "--where",
        "-w",
        nargs=2,
        type=click.Tuple([str, str]),
        help="マッチした行をkey-valueでフィルターする",
    )
    @click.option(
        "--table",
        "style",
        flag_value="table",
        default=True,
        help="table style print",
        show_default=True,
    )
    @click.option(
        "--json",
        "style",
        flag_value="json",
        help="json style print",
        show_default=True,
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
        where: tuple[str, str],
        style: Style,
        pass_command: bool,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        models = func(*args, **kwargs)
        if where is not None:
            models = model_filter(models, key=where[0], value=where[1])
        view(models, keys, style, pass_command)

    return wrapper
