"""exists side effect."""
from __future__ import annotations

import http
from typing import Callable
from uuid import UUID

from pydantic import BaseModel
from requests import HTTPError

from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.vm.domain import AddedVM
from conoha_client.features.vm.errors import (
    VMMemoryShortageError,
)


def post_add_vm(json: dict) -> object:
    """Post func for DI."""
    res = Endpoints.COMPUTE.post("servers", json=json)
    if res.status_code == http.HTTPStatus.BAD_REQUEST:
        msg = res.json()["badRequest"]["message"]
        raise VMMemoryShortageError(msg)
    if res.status_code != http.HTTPStatus.ACCEPTED:
        msg = "なんか想定外のエラーが起きた"
        raise HTTPError(msg)
    return res.json()["server"]


class AddVMCommand(BaseModel, frozen=True):
    """Add New VM Command of CQS Pattern."""

    flavor_id: UUID
    image_id: UUID
    admin_pass: str
    dep: Callable[[dict], object] = post_add_vm

    def __call__(self, sshkey_name: str | None = None) -> AddedVM:
        """新規VM追加."""
        js = {
            "server": {
                "flavorRef": str(self.flavor_id),
                "imageRef": str(self.image_id),
                "adminPass": self.admin_pass,
                "security_groups": [
                    {"name": "default"},
                    {"name": "gncs-ipv4-ssh"},
                    {"name": "gncs-ipv4-all"},
                ],
            },
        }
        if sshkey_name is not None:
            js["server"]["key_name"] = sshkey_name
        res = self.dep(js)
        return AddedVM.model_validate(res)
