"""test repositoy."""


from datetime import timedelta
from typing import Generic, TypeVar

from pydantic import BaseModel

from conoha_client.features.vm.domain import VMStatus

from .domain import Watcher, is_close_or_exceed

T = TypeVar("T")


class Dep(BaseModel, Generic[T]):
    """watcher dependency."""

    pre: T  # switch前の返り値
    post: T  # switch後の返り値
    _switched: bool = False

    def __call__(self) -> T:
        """call."""
        if self._switched:
            return self.post
        return self.pre

    def switch(self) -> None:
        """Switch return."""
        self._switched = True


def test_active2shutoff() -> None:
    """case."""
    dep = Dep(pre=VMStatus.ACTIVE, post=VMStatus.SHUTOFF)
    w = Watcher(expected=VMStatus.SHUTOFF, dep=dep)
    assert not w.is_ok()
    dep.switch()
    assert w.is_ok()


def test_shutoff2active() -> None:
    """case."""
    dep = Dep(pre=VMStatus.SHUTOFF, post=VMStatus.ACTIVE)
    w = Watcher(expected=VMStatus.SHUTOFF, dep=dep)
    assert w.is_ok()
    dep.switch()
    assert not w.is_ok()


def test_is_close() -> None:
    """Practice."""
    elapsed = timedelta(minutes=55)
    plus_charge = timedelta(hours=1)
    assert is_close_or_exceed(elapsed, plus_charge, eps_min=10)
    assert not is_close_or_exceed(elapsed, plus_charge, eps_min=1)
