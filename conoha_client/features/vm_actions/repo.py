"""VM操作 repository."""


from http import HTTPStatus
from typing import Callable
from uuid import UUID

from pydantic import BaseModel
from requests import Response

from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.vm_actions.domain.errors import (
    VMActionTargetNotFoundError,
    VMBootError,
    VMDeleteError,
    VMRebootError,
    VMShutdownError,
    VMSnapshotError,
)


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
        msg = f"削除対象のVM_ID={vm_id}が見つかりませんでした"
        raise VMDeleteError(msg)
    if res.status_code != HTTPStatus.NO_CONTENT:
        msg = f"{vm_id}を削除できませんでした"
        raise VMDeleteError(msg)


ActionDependency = Callable[[UUID, dict], Response]


def action_dep(vm_id: UUID, params: dict) -> Response:
    """VMアクションrequest."""
    res = Endpoints.COMPUTE.post(f"servers/{vm_id}/action", json=params)
    if res.status_code == HTTPStatus.NOT_FOUND:
        msg = f"VM_ID={vm_id}が見つかりませんでした"
        raise VMActionTargetNotFoundError(msg)
    return res


class VMActionCommands(BaseModel, frozen=True):
    """VM action Repository."""

    vm_id: UUID
    dep: ActionDependency = action_dep

    def shutdown(self, is_force: bool = False) -> None:  # noqa: FBT002
        """VMシャットダウン."""
        v = None if is_force else {"force_shutdown": True}
        params = {"os-stop": v}
        res = self.dep(self.vm_id, params)

        if res.status_code != HTTPStatus.ACCEPTED:
            msg = f"{self.vm_id}をシャットダウンできませんでした"
            raise VMShutdownError(msg)

    def boot(self) -> None:
        """VM起動."""
        params = {"os-start": None}
        res = self.dep(self.vm_id, params)

        if res.status_code != HTTPStatus.ACCEPTED:
            msg = f"{self.vm_id}を起動できませんでした"
            raise VMBootError(msg)

    def reboot(self) -> None:
        """VM再起動. HARDは必要になったら作る."""
        params = {"reboot": {"type": "SOFT"}}
        res = self.dep(self.vm_id, params)

        if res.status_code != HTTPStatus.ACCEPTED:
            msg = f"{self.vm_id}を再起動できませんでした"
            raise VMRebootError(msg)

    def snapshot(self, name: str) -> None:
        """VMの状態をイメージとして保存."""
        params = {"createImage": {"name": name}}
        res = self.dep(self.vm_id, params)

        if res.status_code != HTTPStatus.ACCEPTED:
            msg = f"{self.vm_id}をスナップショットできませんでした"
            raise VMSnapshotError(msg)
