"""snapshot shared repository."""

from __future__ import annotations

from typing import Callable
from uuid import UUID

from conoha_client.features._shared.model_list.domain import by, startswith
from conoha_client.features.image.domain.image import Image, ImageList
from conoha_client.features.image.repo import list_images, remove_image
from conoha_client.features.vm_actions.repo import VMActionCommands


def list_snapshots() -> ImageList:
    """List snapshots."""
    return list_images().snapshots


Dependency = Callable[[], ImageList]


def complete_snapshot_by_name(
    pre_name: str,
    dep: Dependency = list_snapshots,
) -> Image:
    """Search snapshot by name prefix match."""
    return dep().find_one_by(startswith("name", pre_name))


def save_snapshot(
    vm_id: UUID,
    name: str,
    dep: Dependency = list_snapshots,
) -> UUID | None:
    """同一名の既存スナップショットがあった場合上書き."""
    old = dep().find_one_or_none_by(by("name", name))
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.snapshot(name)
    if old is not None:
        remove_image(old)
        return old.image_id
    return None
