"""test repositoy."""


from typing import Generic, TypeVar

import pytest
from pydantic import BaseModel

from conoha_client.features.vm.domain import VMStatus
from conoha_client.watch.domain.errors import UnexpectedInitError
from conoha_client.watch.repo.repo import ChangeWatcher

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
    """Valid case."""
    dep = Dep(pre=VMStatus.ACTIVE, post=VMStatus.SHUTOFF)
    w = ChangeWatcher[VMStatus](
        init=VMStatus.ACTIVE,
        post=VMStatus.SHUTOFF,
        dep=dep,
    )
    assert w.initial == dep.pre
    assert not w.is_changed()
    dep.switch()
    assert w.is_changed()


def test_invalid_active2shutoff() -> None:
    """Invalid case."""
    dep = Dep(pre=VMStatus.BUILD, post=VMStatus.SHUTOFF)
    with pytest.raises(UnexpectedInitError):
        ChangeWatcher(init=VMStatus.ACTIVE, post=VMStatus.SHUTOFF, dep=dep)
