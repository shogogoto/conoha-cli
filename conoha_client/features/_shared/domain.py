from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from .view.domain import check_include_keys

T = TypeVar("T", bound=BaseModel)


def find_by_included_prop(models: list[T], key: str, value: str) -> T | None:
    """指定値の文字列が含まれる属性をもつモデルを抽出する."""

    def pred(e: T) -> bool:
        check_include_keys(e, {key})
        return value in str(getattr(e, key))

    ls = filter(pred, models)
    try:
        return next(ls)
    except StopIteration:
        return None


__all__ = ["find_by_included_prop"]
