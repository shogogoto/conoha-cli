"""test repositoy."""


from typing import Generic, TypeVar

from pydantic import BaseModel

from conoha_client.features.vm.domain import VMStatus
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
    """Test case."""
    dep = Dep(pre=VMStatus.ACTIVE, post=VMStatus.SHUTOFF)
    w = ChangeWatcher[VMStatus](expected=VMStatus.SHUTOFF, dep=dep)
    assert w.init == dep.pre
    assert not w()
    dep.switch()
    assert w()
