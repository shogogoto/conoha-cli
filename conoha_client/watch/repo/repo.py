"""watch repo."""
from __future__ import annotations

import operator
import time
from typing import Any, Callable, Generic, TypeVar
from uuid import UUID

import click
from pydantic import BaseModel

from conoha_client._shared.snapshot.repo import save_snapshot
from conoha_client.features.vm.domain import VMStatus
from conoha_client.features.vm_actions.repo import VMActionCommands, remove_vm
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


def stopped_vm(vm_id: UUID) -> None:
    """VM stop."""
    Watcher(
        expected=VMStatus.SHUTOFF,
        dep=vm_status_finder(vm_id),
    ).wait_for(
        callback=lambda: VMActionCommands(vm_id=vm_id).shutdown(),
        interval_sec=1,
    )


def saved_vm(vm_id: UUID, name: str) -> None:
    """VM saved."""
    Watcher(
        expected=100,
        dep=snapshot_progress_finder(name),
        view=lambda x: click.echo(f"save progress is {x}%"),
    ).wait_for(
        callback=lambda: save_snapshot(vm_id, name),
        interval_sec=10,
    )


def removed_vm(vm_id: UUID) -> None:
    """VM Removed."""
    Watcher(
        expected=False,
        dep=exists_vm(vm_id),
    ).wait_for(
        callback=lambda: remove_vm(vm_id),
        interval_sec=1,
    )
