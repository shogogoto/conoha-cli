from __future__ import annotations

from typing import Callable, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def first_model_by(models: list[T], pred: Callable[T, bool]) -> T | None:
    """条件を満たしたモデルを抽出する."""
    ls = filter(pred, models)
    try:
        return next(ls)
    except StopIteration:
        return None


__all__ = ["first_model_by"]
