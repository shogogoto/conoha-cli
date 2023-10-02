"""VM Create API."""
from __future__ import annotations

import operator
from functools import cache, cached_property
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from pydantic import BaseModel

from conoha_client.features._shared import view
from conoha_client.features.image.repo import list_images
from conoha_client.features.plan.repo import first_vmplan_by

from .domain.errors import (
    ImageIdMappingMismatchWarning,
    NotFoundApplicationError,
    NotFoundFlavorIdError,
    NotFoundOSVersionError,
)

if TYPE_CHECKING:
    from conoha_client.add_vm.domain.domain import Application
    from conoha_client.features.image.domain import Image

from .domain import OS, Memory, OSVersion  # noqa: TCH001


@cache
def list_image_names() -> list[str]:
    """VM Image名一覧."""
    return [img.name for img in list_images()]


Callback = Callable[[], list[str]]  # list_image_names関数の型


class ImageInfoRepo(BaseModel, frozen=True):
    """VM Imageに関するリポジトリ."""

    memory: Memory
    os: OS
    list_image: Callback = list_images

    @cached_property
    def image_names(self) -> list[str]:
        """イメージ名一覧."""
        return [img.name for img in list_images()]

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

        res = list(filter(pred, list_images()))
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


def add_vm(mem: Memory, os: OS, app: Application) -> None:
    """新規VM追加."""
    print(mem, os, app)  # noqa: T201
    # print(find_image_id(mem, os, app))
    # plan = find_vmplan_by("name", mem.expression)

    # def pred(img: Image) -> bool:
    #     in_os = os_.value in img.name
    #     in_app = app.value in img.app
    #     return in_os and in_app

    # image = filter_model_by(list_images(), pred)
    # print(image)
    # js = {"flavorRef": plan.flavor_id, "imageRef": image.image_id}
    # print(js)
    # Endpoints.COMPUTE.post("servers", json=js)
