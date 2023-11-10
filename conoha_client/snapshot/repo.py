"""snapshot repository."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable
from uuid import UUID

from conoha_client.features._shared.model_list.domain import by, startswith
from conoha_client.features.image.domain.image import Image, ImageList
from conoha_client.features.image.repo import list_images, remove_image
from conoha_client.features.plan.repo import find_vmplan
from conoha_client.features.vm.repo.command import AddVMCommand
from conoha_client.features.vm_actions.repo import VMActionCommands

if TYPE_CHECKING:
    from conoha_client.features.plan.domain import Memory
    from conoha_client.features.vm.domain import AddedVM


def list_snapshots() -> ImageList:
    """List snapshots."""
    return list_images().snapshots


def complete_snapshot(
    pre_uid: str,
    dep: Dependency = list_snapshots,
) -> Image:
    """Search snapshot by uuid prefix match."""
    return dep().find_one_by(startswith("image_id", pre_uid))


def complete_snapshot_by_name(
    pre_name: str,
    dep: Dependency = list_snapshots,
) -> Image:
    """Search snapshot by name prefix match."""
    return dep().find_one_by(startswith("name", pre_name))


Dependency = Callable[[], ImageList]


def save_snapshot(
    vm_id: UUID,
    name: str,
    dep: Dependency = list_snapshots,
) -> bool:
    """同一名の既存スナップショットがあった場合上書き."""
    old = dep().find_one_or_none_by(by("name", name))
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.snapshot(name)
    exists_old = old is not None
    if exists_old:
        remove_image(old)
    return exists_old


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
