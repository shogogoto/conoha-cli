"""watch repo."""
from __future__ import annotations

import time
from typing import Callable, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

from conoha_client._shared.snapshot.repo import complete_snapshot_by_name, save_snapshot
from conoha_client.features.vm.domain import VMStatus
from conoha_client.features.vm_actions.repo import VMActionCommands, remove_vm
from conoha_client.watch.domain.event import VMRemoved, VMSaved, VMStopped
from conoha_client.watch.repo.memo import (
    exists_vm,
    snapshot_progress_finder,
    vm_status_finder,
)

T = TypeVar("T")


class Watcher(BaseModel, Generic[T], frozen=True):
    """watch VM State change."""

    expected: T
    dep: Callable[[], T]

    def is_ok(self) -> bool:
        """Is satisfied as expected."""
        return self.dep() == self.expected


def stopped_vm(vm_id: UUID) -> VMStopped:
    """VM stop."""
    w = Watcher(
        expected=VMStatus.SHUTOFF,
        dep=vm_status_finder(vm_id),
    )
    if not w.is_ok():
        cmd = VMActionCommands(vm_id=vm_id)
        cmd.shutdown()

    while not w.is_ok():
        time.sleep(10)
    return VMStopped(vm_id=vm_id)


def saved_vm(vm_id: UUID, name: str) -> VMSaved:
    """VM saved."""
    save_snapshot(vm_id, name)
    w = Watcher(
        expected=100,
        dep=snapshot_progress_finder(name),
    )

    while not w.is_ok():
        time.sleep(10)
    image = complete_snapshot_by_name(name)
    return VMSaved(vm_id=vm_id, snapshot_id=image.image_id)


def removed_vm(vm_id: UUID) -> VMRemoved:
    """Remove VM."""
    w = Watcher(
        expected=False,
        dep=exists_vm(vm_id),
    )
    remove_vm(vm_id=vm_id)
    while not w.is_ok():
        time.sleep(10)
    return VMRemoved(vm_id=vm_id)
