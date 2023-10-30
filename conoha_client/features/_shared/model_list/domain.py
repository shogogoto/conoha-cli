from __future__ import annotations

from typing import Any, Callable, Iterator, TypeVar

from pydantic import BaseModel, RootModel

from conoha_client.features._shared.view.domain import check_include_keys

T = TypeVar("T", bound=BaseModel)


Predicate = Callable[[T], bool]


def by(attr: str, value: Any) -> Predicate:  # noqa: ANN401
    """Create image predicate."""

    def pred(model: T) -> bool:
        check_include_keys(model.__class__, {attr})
        return getattr(model, attr) == value

    return pred


def startswith(attr: str, starts: str) -> Predicate:
    """前方一致."""

    def pred(model: T) -> bool:
        check_include_keys(model.__class__, {attr})
        val = getattr(model, attr)
        return str(val).startswith(starts)

    return pred


class ModelList(RootModel[list[T]], frozen=True):
    """base."""

    root: list[T]

    def __iter__(self) -> Iterator[T]:
        """Behavior like list."""
        return iter(self.root)

    def __next__(self) -> T:
        """Behavior like list."""
        return next(self.root)

    def __len__(self) -> int:
        """Count of elements."""
        return len(self.root)

    def __getitem__(self, i: int) -> T:
        """Indexing."""
        return self.root[i]

    def find_one_by(self, pred: Callable[[T], bool]) -> T:
        """Find only image by predicate."""
        one = self.find_one_or_none_by(pred)
        if one is None:
            raise NotMatchError
        return one

    def find_one_or_none_by(self, pred: Callable[[T], bool]) -> T | None:
        """Find one or not found."""
        founds = list(filter(pred, self.root))
        n = len(founds)
        if n == 0:
            return None
        if n == 1:
            return founds[0]
        raise MultipleMatchError


class NotMatchError(Exception):
    """ひとつだけマッチすることを期待したのに."""


class MultipleMatchError(Exception):
    """複数のイメージがマッチするの許さないお."""
