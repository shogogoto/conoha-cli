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
    from conoha_client.features.image.domain.operating_system import Distribution
    from conoha_client.features.list_vm.domain import Server
    from conoha_client.features.plan.domain import Memory

Callback = Callable[[], LinuxImageList]


def list_linux_images() -> LinuxImageList:
    """Fix in future."""
    return ImageList(list_images()).priors.linux


def available_dist_versions(
    memory: Memory,
    dist: Distribution,
    dep: Callback = list_linux_images,
) -> set[str]:
    """List availabe distribution versions."""
    lins = dep()
    return filter_memory(lins, memory).dist_versions(dist)


def available_dist_latest_version(
    memory: Memory,
    dist: Distribution,
    dep: Callback = list_linux_images,
) -> str:
    """Latest availabe distribution version."""
    vers = available_dist_versions(memory, dist, dep)
    return sorted(vers)[-1]


def available_apps(
    memory: Memory,
    dist: Distribution,
    dist_version: str,
    dep: Callback = list_linux_images,
) -> set[str]:
    """引数のOS,versionで利用可能なアプリ,バージョン一覧."""
    lins = dep()
    return filter_memory(lins, memory).applications(dist, dist_version)


def identify_image(
    memory: Memory,
    dist: Distribution,
    dist_version: str,
    app: str,
    dep: Callback = list_linux_images,
) -> Image:
    """imageを一意に検索する."""
    lins = dep()
    return select_uniq(lins, memory, dist, dist_version, app)


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
