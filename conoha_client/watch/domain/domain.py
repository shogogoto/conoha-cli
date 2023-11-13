"""watch domain."""
from __future__ import annotations

import operator
import time
from datetime import timedelta
from typing import Any, Callable, Generic, TypeVar

from pydantic import BaseModel

from conoha_client.features._shared.util import now_jst

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
    ) -> timedelta:
        """Wait for reflecting the callback."""
        callback()
        started = now_jst()
        while not self.is_ok():
            time.sleep(interval_sec)
        return now_jst() - started


def is_close_or_exceed(
    x: timedelta,
    deadline: timedelta,
    eps_min: int,
) -> bool:
    """差がeps以内か超えるか."""
    if x > deadline:
        return True

    return abs(x - deadline) < timedelta(minutes=eps_min)
