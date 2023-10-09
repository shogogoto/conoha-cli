"""VM操作 repository."""


from http import HTTPStatus
from typing import Callable
from uuid import UUID

from requests import Response

from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.vm_actions.domain.errors import VMDeleteError


def remove_dep(vm_id: UUID) -> Response:
    """VM削除request."""
    return Endpoints.COMPUTE.delete(f"servers/{vm_id}")


def remove_vm(
    vm_id: UUID,
    dep: Callable[[UUID], Response] = remove_dep,
) -> None:
    """VM削除."""
    res = dep(vm_id)
    if res.status_code == HTTPStatus.NOT_FOUND:
        msg = "削除対象のVM_IDが見つかりませんでした"
        raise VMDeleteError(msg)
    if res.status_code != HTTPStatus.NO_CONTENT:
        msg = f"{vm_id}は何らかの理由でVMが削除できませんでした"
        raise VMDeleteError(msg)
