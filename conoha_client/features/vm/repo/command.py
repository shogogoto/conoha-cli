"""exists side effect."""
from __future__ import annotations

import http
from typing import Callable
from uuid import UUID

from pydantic import BaseModel
from requests import HTTPError

from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.vm.domain import VM, AddedVM
from conoha_client.features.vm.errors import (
    NotFlavorProvidesError,
    NotFoundAddedVMError,
)
from conoha_client.features.vm.repo.query import get_dep, list_servers


def post_add_vm(json: dict) -> object:
    """Post func for DI."""
    res = Endpoints.COMPUTE.post("servers", json=json)
    if res.status_code == http.HTTPStatus.BAD_REQUEST:
        msg = (
            "そのイメージとプランの組み合わせは提供されていません."
            "別の組み合わせをお試しください"
        )
        raise NotFlavorProvidesError(msg)
    if res.status_code != http.HTTPStatus.ACCEPTED:
        msg = "なんか想定外のエラーが起きた"
        raise HTTPError(msg)
    return res.json()["server"]


class AddVMCommand(BaseModel, frozen=True):
    """Add New VM Command of CQS Pattern."""

    flavor_id: UUID
    image_id: UUID
    admin_pass: str
    post: Callable[[dict], object] = post_add_vm

    def __call__(self, sshkey_name: str | None = None) -> AddedVM:
        """新規VM追加."""
        js = {
            "server": {
                "flavorRef": str(self.flavor_id),
                "imageRef": str(self.image_id),
                "adminPass": self.admin_pass,
            },
        }
        if sshkey_name is not None:
            js["server"]["key_name"] = sshkey_name
        res = self.post(js)
        return AddedVM.model_validate(res)


def find_added(
    vm_id: UUID,
    dep: Callable[[], list[object]] = get_dep,
) -> VM:
    """Return ipv4 of added vm."""

    def pred(vm: VM) -> bool:
        return vm.vm_id == vm_id

    f = filter(pred, list_servers(dep=dep))

    try:
        return next(f)
    except StopIteration as e:
        msg = ""
        raise NotFoundAddedVMError(msg) from e
