"""watch domain."""
from __future__ import annotations

import operator
import time
from datetime import timedelta
from typing import Any, Callable, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Watcher(BaseModel, Generic[T], frozen=True):
    """watch VM State change."""

    expected: T
    dep: Callable[[], T]
    view: Callable[[T], Any] | None = None
    ok: Callable[[T, T], bool] = operator.eq

    def is_ok(self) -> bool:
        """Is satisfied as expected."""
        v = self.dep()
        if self.view is not None:
            self.view(v)
        return self.ok(v, self.expected)

    def wait_for(
        self,
        callback: Callable[[], Any],
        interval_sec: int,
    ) -> None:
        """Wait for reflecting the callback."""
        callback()
        while not self.is_ok():
            time.sleep(interval_sec)


def is_close(x: timedelta, y: timedelta, eps_min: int) -> bool:
    """差がeps以内か."""
    return abs(x - y) < timedelta(minutes=eps_min)
