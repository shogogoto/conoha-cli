"""snapshot repository."""


from uuid import UUID

from conoha_client.features.image.domain.image import ImageList
from conoha_client.features.image.repo import list_images
from conoha_client.features.vm_actions.repo import VMActionCommands


def list_snapshots() -> ImageList:
    """List snapshots."""
    return list_images().snapshots


def save_snapshot(vm_id: UUID, name: str) -> None:
    """同一名の既存スナップショットがあった場合上書き."""
    cmd = VMActionCommands(vm_id=vm_id)
    cmd.snapshot(name)
