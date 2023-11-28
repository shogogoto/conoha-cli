"""VM操作 repository."""
from __future__ import annotations

from http import HTTPStatus
from typing import Callable
from uuid import UUID

from pydantic import BaseModel
from requests import Response

from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.vm.repo.query import complete_vm
from conoha_client.features.vm_actions.domain.errors import (
    VMActionConflictingError,
    VMActionTargetNotFoundError,
    VMBootError,
    VMDeleteError,
    VMRebootError,
    VMRebuildError,
    VMResizeError,
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
    if res.status_code == HTTPStatus.CONFLICT:
        msg = res.json()["conflictingRequest"]["message"]
        raise VMActionConflictingError(msg)
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
            rmsg = res.json()["message"]
            msg = f"{self.vm_id}をスナップショットできませんでした.{rmsg}"
            raise VMSnapshotError(msg)

    def resize(self, flavor_id: UUID) -> None:
        """VMのmemoryを変更."""
        params = {"resize": {"flavorRef": str(flavor_id)}}
        res = self.dep(self.vm_id, params)
        if res.status_code == HTTPStatus.BAD_REQUEST:
            msg = "メモリ512MGプランから1G,2G,...プランへの変更またはその逆はできません"
            vm = complete_vm(str(self.vm_id))
            if vm.flavor_id == flavor_id:
                msg = "変更前と異なるメモリを指定してください"
            raise VMResizeError(msg)
        if res.status_code != HTTPStatus.ACCEPTED:
            msg = f"{self.vm_id}をプラン変更できませんでした"
            VMResizeError(msg)

    def confirm_resize(self) -> None:
        """memory変更を確定."""
        params = {"confirmResize": None}
        res = self.dep(self.vm_id, params)
        if res.status_code != HTTPStatus.NO_CONTENT:
            msg = f"{self.vm_id}のプラン変更確定に失敗しました"
            raise VMResizeError(msg)

    def revert_resize(self) -> None:
        """memory変更を取り消し."""
        params = {"revertResize": None}
        res = self.dep(self.vm_id, params)
        if res.status_code != HTTPStatus.ACCEPTED:
            msg = f"{self.vm_id}のプラン変更取消に失敗しました"
            raise VMResizeError(msg)

    def rebuild(
        self,
        image_id: UUID,
        admin_pass: str,
        sshkey_name: str | None = None,
    ) -> None:
        """imageを既存VMへ再インストール."""
        params = {
            "rebuild": {
                "imageRef": str(image_id),
                "adminPass": admin_pass,
            },
        }
        if sshkey_name is not None:
            params["rebuild"]["key_name"] = sshkey_name
        res = self.dep(self.vm_id, params)
        if res.status_code != HTTPStatus.ACCEPTED:
            msg = f"f{self.vm_id}へのOS再インストールに失敗しました"
            raise VMRebuildError(msg)
