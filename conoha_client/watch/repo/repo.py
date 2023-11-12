"""watch repo."""
from __future__ import annotations

from datetime import timedelta
from uuid import UUID

import click

from conoha_client._shared.snapshot.repo import save_snapshot
from conoha_client.features.vm.domain import VMStatus
from conoha_client.features.vm_actions.repo import VMActionCommands, remove_vm
from conoha_client.watch.domain.domain import Watcher, is_close
from conoha_client.watch.repo.memo import (
    elapsed_from_created,
    exists_vm,
    snapshot_progress_finder,
    vm_status_finder,
)


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


def wait_plus_charge(vm_id: UUID) -> None:
    """次の時間課金が迫ってきた.

    VMは作成後の経過時間に対して1時間単位で課金される.
    追加課金される5分前まで待つ
    """
    Watcher(
        expected=timedelta(hours=1),
        dep=elapsed_from_created(vm_id),
        view=lambda x: click.echo(f"elapsed: {x}"),
        ok=lambda x, y: is_close(x, y, eps_min=5),
    ).wait_for(
        callback=lambda: ...,
        interval_sec=60,  # 60secごとしか更新されない
    )
