"""watch repo."""
from __future__ import annotations

from functools import cached_property
from typing import Callable, Generic, TypeVar

from pydantic import BaseModel

# def finish() -> None:
#     """VM利用を終了する."""
#     # vm stop
#     # snapshot save
#     # vm remove
#     # VMのステータスが変わるまで待たねばならない


# def stop(vm_id: UUID) -> VMStopped:
#     """VM stop."""
#     cmd = VMActionCommands(vm_id=vm_id)
#     cmd.shutdown()
#     return VMStopped(vm_id=vm_id)


# def save(vm_id: UUID, name: str) -> VMSaved:
#     save_snapshot(vm_id, name)
#     # complete_snapshot_by_name(name)


# # def wait_for():
# #     """API実行がされるまで待つ."""
# def find_vm_by_id(vm_id: UUID) -> VM:
#     """Find VM."""
#     return complete_vm(str(vm_id))


T = TypeVar("T")

Dependency = Callable[[], T]


# frozenならthreading localを満たす
class ChangeWatcher(BaseModel, Generic[T], frozen=True):
    """watch VM State change."""

    expected: T
    dep: Dependency

    @cached_property
    def init(self) -> T:
        """Cache."""
        return self.dep()

    def model_post_init(self, _: None) -> None:
        """Cache initial dep return."""
        self.init  # noqa: B018

    def __call__(self) -> bool:
        """Is changed from init."""
        now = self.dep()
        if now == self.init:
            return False
        return now == self.expected
