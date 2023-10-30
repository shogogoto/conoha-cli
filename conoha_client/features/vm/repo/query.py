"""契約中VM API."""
from __future__ import annotations

from typing import Callable
from uuid import UUID

from conoha_client.features._shared import Endpoints
from conoha_client.features.vm.domain import VM
from conoha_client.features.vm.errors import NotFoundAddedVMError


def get_dep() -> list[object]:
    """For Dependency Injection."""
    res = Endpoints.COMPUTE.get("servers/detail").json()
    return res["servers"]


def list_vms(
    dep: Callable[[], list[object]] = get_dep,
) -> list[VM]:
    """契約中のサーバー情報一覧を取得する."""
    res = dep()
    return [VM.model_validate(e) for e in res]


def find_added(
    vm_id: UUID,
    dep: Callable[[], list[object]] = get_dep,
) -> VM:
    """Return ipv4 of added vm."""

    def pred(vm: VM) -> bool:
        return vm.vm_id == vm_id

    f = filter(pred, list_vms(dep=dep))

    try:
        return next(f)
    except StopIteration as e:
        msg = ""
        raise NotFoundAddedVMError(msg) from e
