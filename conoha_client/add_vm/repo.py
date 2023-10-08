"""VM Create API."""
from __future__ import annotations

import http
import operator
from functools import cached_property
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from pydantic import BaseModel
from requests import HTTPError

from conoha_client.add_vm.domain.added_vm import AddedVM
from conoha_client.features._shared import view
from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.image.repo import list_images
from conoha_client.features.list_vm.repo import get_dep, list_servers
from conoha_client.features.plan.repo import first_vmplan_by

from .domain.errors import (
    ImageIdMappingMismatchWarning,
    NotFlavorProvidesError,
    NotFoundAddedVMError,
    NotFoundApplicationError,
    NotFoundFlavorIdError,
    NotFoundOSVersionError,
)

if TYPE_CHECKING:
    from conoha_client.add_vm.domain.domain import Application
    from conoha_client.features.image.domain import Image
    from conoha_client.features.list_vm.domain import Server

from .domain import OS, Memory, OSVersion  # noqa: TCH001


class ImageInfoRepo(BaseModel, frozen=True):
    """VM Imageに関するリポジトリ."""

    memory: Memory
    os: OS
    list_images: Callable[[], list[str]] = list_images

    @cached_property
    def image_names(self) -> list[str]:
        """イメージ名一覧."""
        return [img.name for img in self.list_images()]

    @cached_property
    def available_os_versions(self) -> list[OSVersion]:
        """利用可能なOSバージョンを取得."""
        mem_names = filter(self.memory.is_match, self.image_names)
        s = set(filter(self.os.is_match, mem_names))
        return sorted({self.os.version(n) for n in s}, key=operator.attrgetter("value"))

    @cached_property
    def available_os_latest_version(self) -> OSVersion:
        """利用可能な最新OSバージョンを取得."""
        vers = self.available_os_versions
        if len(vers) == 0:
            raise NotFoundOSVersionError
        return vers[-1]

    def list_available_apps(self, os_version: OSVersion) -> list[Application]:
        """引数のOS,versionで利用可能なアプリ,バージョン一覧."""
        os_versions = self.available_os_versions
        if os_version.is_latest():
            os_version = self.available_os_latest_version
        if os_version not in os_versions:
            msg = (
                f"{self.os}のバージョン{os_version.value}は利用できません."
                f"利用可能なバージョンは{[v.value for v in os_versions]}です"
            )
            raise NotFoundOSVersionError(msg)
        mem_names = filter(self.memory.is_match, self.image_names)
        os_names = filter(self.os.is_match, mem_names)
        ver_names = filter(os_version.is_match, os_names)
        appsv = [self.os.app_with_version(n) for n in ver_names]
        return sorted(appsv, key=operator.attrgetter("name"))

    def find_image_id(self, os_version: OSVersion, app: Application) -> UUID:
        """指定条件からimage idを一意に検索する."""
        if os_version.is_latest():
            os_version = self.available_os_latest_version
        if os_version not in self.available_os_versions:
            raise NotFoundOSVersionError

        if app not in self.list_available_apps(os_version):
            raise NotFoundApplicationError

        def pred(img: Image) -> bool:
            n = img.name

            return (
                self.memory.is_match(n)
                and self.os.is_match(n)
                and os_version.is_match(n)
                and app.is_match(n, self.os)
            )

        res = list(filter(pred, self.list_images()))
        if len(res) != 1:
            view(res, keys={}, style="table", pass_command=False)
            raise ImageIdMappingMismatchWarning

        return res[0].image_id


def find_plan_id(memory: Memory) -> UUID:
    """メモリ容量からFlavor IDをみつける."""
    flavor = first_vmplan_by("name", memory.expression)
    if flavor is None:
        msg = f"{memory.value}GBのプランIDがみつかりませんでした"
        raise NotFoundFlavorIdError(msg)
    return flavor.flavor_id


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
