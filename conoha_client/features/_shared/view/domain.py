"""CLI表示用モデル変換."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel


class ExtraKeyError(Exception):
    """View表示keysにモデルプロパィにない値が指定された."""


def model_filter(model: BaseModel, keys: set[str] | None = None) -> object:
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
