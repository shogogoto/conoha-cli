"""query memorize."""


from datetime import timedelta
from typing import Callable
from uuid import UUID

from conoha_client._shared.snapshot.repo import complete_snapshot_by_name
from conoha_client.features._shared.model_list.domain import ModelList, by
from conoha_client.features.vm.domain import VMStatus
from conoha_client.features.vm.repo.query import complete_vm, list_vms


def vm_status_finder(vm_id: UUID) -> Callable[[], VMStatus]:
    """Find status by id. memo."""

    def _f() -> VMStatus:
        vm = complete_vm(str(vm_id))
        return vm.status

    return _f


def snapshot_progress_finder(name: str) -> Callable[[], int]:
    """Find progress by name memo."""

    def _f() -> int:
        image = complete_snapshot_by_name(name)
        return image.progress

    return _f


def exists_vm(vm_id: UUID) -> Callable[[], bool]:
    """Exists vm memo."""

    def _f() -> bool:
        vm = ModelList(list_vms()).find_one_or_none_by(by("vm_id", vm_id))
        return vm is not None

    return _f


def elapsed_from_created(vm_id: UUID) -> Callable[[], timedelta]:
    """Elapsed time memo."""

    def _f() -> timedelta:
        vm = complete_vm(str(vm_id))
        return vm.elapsed_from_created()

    return _f
