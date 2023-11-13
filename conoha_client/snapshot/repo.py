"""snapshot repository."""
from __future__ import annotations

from typing import TYPE_CHECKING

from conoha_client._shared.snapshot.repo import (
    complete_snapshot_by_name,
    list_snapshots,
)
from conoha_client.features.plan.repo import find_vmplan
from conoha_client.features.vm.repo.command import AddVMCommand

if TYPE_CHECKING:
    from conoha_client._shared.snapshot.repo import Dependency
    from conoha_client.features.image.domain.image import Image
    from conoha_client.features.plan.domain import Memory
    from conoha_client.features.vm.domain import AddedVM


def restore_snapshot(
    pre_name: str,
    memory: Memory,
    admin_password: str,
    keypair_name: str,
    dep: Dependency = list_snapshots,
) -> tuple[AddedVM, Image]:
    """スナップショットからVMを復元する."""
    img = complete_snapshot_by_name(pre_name, dep)
    cmd = AddVMCommand(
        flavor_id=find_vmplan(memory).flavor_id,
        image_id=img.image_id,
        admin_pass=admin_password,
    )
    return cmd(keypair_name), img
