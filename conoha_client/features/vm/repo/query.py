"""契約中VM API."""
from __future__ import annotations

from functools import cache
from typing import Callable
from uuid import UUID

from conoha_client.features._shared import Endpoints
from conoha_client.features._shared.model_list.domain import ModelList, startswith
from conoha_client.features.vm.domain import VM
from conoha_client.features.vm.errors import NotFoundAddedVMError


def get_dep() -> list[object]:
    """For Dependency Injection."""
    res = Endpoints.COMPUTE.get("servers/detail").json()
    return res["servers"]


@cache
def list_vms(
    dep: Callable[[], list[object]] = get_dep,
) -> list[VM]:
    """契約中のサーバー情報一覧を取得する."""
    res = dep()
    return [VM.model_validate(e) for e in res]


def complete_vm(s: str) -> VM:
    """uuidを補完して検索."""
    return ModelList[VM](list_vms()).find_one_by(startswith("vm_id", s))


def complete_vm_id(s: str) -> UUID:
    """uuidを補完して検索."""
    return complete_vm(s).vm_id


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
