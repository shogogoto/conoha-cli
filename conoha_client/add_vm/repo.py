"""VM Create API."""
from __future__ import annotations

import http
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from pydantic import BaseModel
from requests import HTTPError

from conoha_client.add_vm.domain.added_vm import AddedVM
from conoha_client.add_vm.domain.domain import filter_memory, select_uniq
from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.image.domain.image import ImageList, LinuxImageList
from conoha_client.features.image.repo import list_images
from conoha_client.features.list_vm.repo import get_dep, list_servers

from .domain.errors import (
    NotFlavorProvidesError,
    NotFoundAddedVMError,
)

if TYPE_CHECKING:
    from conoha_client.features.image.domain import Image
    from conoha_client.features.list_vm.domain import Server

from conoha_client.features.image.domain.operating_system import (
    Distribution,  # noqa: TCH001
)
from conoha_client.features.plan.domain import Memory  # noqa: TCH001

Callback = Callable[[], LinuxImageList]


def list_linux_images() -> LinuxImageList:
    """Fix in future."""
    return ImageList(list_images()).priors.linux


class DistQuery(BaseModel, frozen=True):
    """Linux image query to add new VM."""

    memory: Memory
    dist: Distribution
    dep: Callback = list_linux_images

    def _filter_mem(self) -> LinuxImageList:
        return filter_memory(self.dep(), self.memory)

    def available_vers(self) -> set[str]:
        """List availabe distribution versions."""
        return self._filter_mem().dist_versions(self.dist)

    def latest_ver(self) -> str:
        """Latest availabe distribution version."""
        return sorted(self.available_vers())[-1]

    def apps(self, dist_ver: str) -> set[str]:
        """引数のOS,versionで利用可能なアプリ,バージョン一覧."""
        return self._filter_mem().applications(self.dist, dist_ver)

    def identify(self, dist_ver: str, app: str) -> Image:
        """Linux Imageを一意に検索する."""
        return select_uniq(
            self.dep(),
            self.memory,
            self.dist,
            dist_ver,
            app,
        )


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
) -> Server:
    """Return ipv4 of added vm."""

    def pred(vm: Server) -> bool:
        return vm.vm_id == vm_id

    f = filter(pred, list_servers(get=dep))

    try:
        return next(f)
    except StopIteration as e:
        msg = ""
        raise NotFoundAddedVMError(msg) from e
