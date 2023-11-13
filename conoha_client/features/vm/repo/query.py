"""契約中VM API."""
from __future__ import annotations

from typing import Callable
from uuid import UUID

from conoha_client.features._shared import Endpoints
from conoha_client.features._shared.model_list.domain import ModelList, startswith
from conoha_client.features.vm.domain import VM


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


def complete_vm(s: str) -> VM:
    """uuidを補完して検索."""
    return ModelList[VM](list_vms()).find_one_by(startswith("vm_id", s))


def complete_vm_id(s: str) -> UUID:
    """uuidを補完して検索."""
    return complete_vm(s).vm_id
