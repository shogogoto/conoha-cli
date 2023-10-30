"""snapshot repository."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable
from uuid import UUID

from conoha_client.features.image.domain.image import Image, ImageList
from conoha_client.features.image.repo import list_images, remove_image
from conoha_client.features.plan.repo import find_vmplan
from conoha_client.features.vm.repo.command import AddVMCommand
from conoha_client.features.vm_actions.repo import VMActionCommands
from conoha_client.snapshot.domain import by

if TYPE_CHECKING:
    from conoha_client.features.plan.domain import Memory
    from conoha_client.features.vm.domain import AddedVM


def list_snapshots() -> ImageList:
    """List snapshots."""
    return list_images().snapshots


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
    image_id: UUID,
    memory: Memory,
    admin_password: str,
    keypair_name: str,
    dep: Dependency = list_snapshots,
) -> tuple[AddedVM, Image]:
    """スナップショットからVMを復元する."""
    img = dep().find_by_id(image_id)
    cmd = AddVMCommand(
        flavor_id=find_vmplan(memory).flavor_id,
        image_id=img.image_id,
        admin_pass=admin_password,
    )
    return cmd(keypair_name), img


def remove_snapshot(
    image_id: UUID,
    dep: Dependency = list_snapshots,
) -> Image:
    """スナップショットをID指定で削除."""
    one = dep().find_one_by(by("image_id", image_id))
    remove_image(one)
    return one
