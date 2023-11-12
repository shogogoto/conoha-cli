"""watch repo."""
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Callable, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

from conoha_client.features.vm.repo.query import complete_vm
from conoha_client.features.vm_actions.repo import VMActionCommands
from conoha_client.watch.domain.errors import UnexpectedInitError
from conoha_client.watch.domain.event import VMStopped

if TYPE_CHECKING:
    from conoha_client.features.vm.domain import VMStatus

# def finish() -> None:
#     """VM利用を終了する."""
#     # vm stop
#     # snapshot save
#     # vm remove
#     # VMのステータスが変わるまで待たねばならない


# def save(vm_id: UUID, name: str) -> VMSaved:
#     save_snapshot(vm_id, name)
#     # complete_snapshot_by_name(name)


# # def wait_for():
# #     """API実行がされるまで待つ."""
# def find_vm_by_id(vm_id: UUID) -> VM:
#     """Find VM."""
#     return complete_vm(str(vm_id))


T = TypeVar("T")


class ChangeWatcher(BaseModel, Generic[T], frozen=True):
    """watch VM State change."""

    init: T
    post: T
    dep: Callable[[], T]

    @cached_property
    def initial(self) -> T:
        """Cache first return of dependency."""
        return self.dep()

    def model_post_init(self, _: None) -> None:
        """Cache initial dep return."""
        if self.initial != self.init:
            raise UnexpectedInitError

    def is_changed(self) -> bool:
        """Is changed from init."""
        now = self.dep()
        if now == self.initial:
            return False
        return now == self.post


def vm_status_finder(vm_id: UUID) -> Callable[[], VMStatus]:
    """Find status by id."""

    def _func() -> VMStatus:
        return complete_vm(str(vm_id)).status

    return _func


def stop(vm_id: UUID) -> VMStopped:
    """VM stop."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.shutdown()
    return VMStopped(vm_id=vm_id)
