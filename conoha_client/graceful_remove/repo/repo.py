"""watch repo."""
from __future__ import annotations

from datetime import timedelta
from uuid import UUID

import click

from conoha_client._shared.snapshot.repo import save_snapshot
from conoha_client.features.vm.domain import VMStatus
from conoha_client.features.vm_actions.repo import VMActionCommands
from conoha_client.graceful_remove.domain import Watcher, is_close_or_exceed

from .curry import (
    elapsed_from_created,
    snapshot_progress_finder,
    vm_status_finder,
)


def stopped_vm(vm_id: UUID) -> timedelta:
    """VM stop."""
    watch = vm_status_finder(vm_id)

    if watch() == VMStatus.SHUTOFF:

        def callback() -> None:
            pass
    else:

        def callback() -> None:
            return VMActionCommands(vm_id=vm_id).shutdown()

    return Watcher(
        expected=VMStatus.SHUTOFF,
        dep=watch,
    ).wait_for(
        callback=callback,
        interval_sec=1,
    )


def saved_vm(vm_id: UUID, name: str) -> timedelta:
    """VM saved."""
    return Watcher(
        expected=100,
        dep=snapshot_progress_finder(name),
        view=lambda x: click.echo(f"save progress is {x}%"),
    ).wait_for(
        callback=lambda: save_snapshot(vm_id, name),
        interval_sec=10,
    )


def wait_plus_charge(
    vm_id: UUID,
    within_min: int,
    deadline_min: int = 60,
) -> None:
    """次の時間課金が迫ってきた.

    VMは作成後の経過時間に対して1時間単位で課金される.
    追加課金される5分前まで待つ
    """
    Watcher(
        expected=timedelta(minutes=deadline_min),
        dep=elapsed_from_created(vm_id),
        view=lambda x: click.echo(f"elapsed from created VM({vm_id}): {x}"),
        ok=lambda x, y: is_close_or_exceed(x, y, eps_min=within_min),
    ).wait_for(
        callback=lambda: ...,
        interval_sec=60,  # 60secごとしかqueryが更新されない
    )
