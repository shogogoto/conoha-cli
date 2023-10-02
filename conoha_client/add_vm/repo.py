"""VM Create API."""
from __future__ import annotations

import operator
from functools import cache
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from conoha_client.features._shared import view
from conoha_client.features.image.repo import list_images
from conoha_client.features.plan import first_vmplan_by

from .domain import OS, Memory, NotFoundFlavorIdError, OSVersion
from .domain.errors import (
    ImageIdMappingMismatchWarning,
    NotFoundApplicationError,
    NotFoundOSVersionError,
)

if TYPE_CHECKING:
    from conoha_client.add_vm.domain.domain import Application
    from conoha_client.features.image.domain import Image


@cache
def list_image_names() -> list[str]:
    """VM Image名一覧."""
    return [img.name for img in list_images()]


Callback = Callable[[], list[str]]  # list_image_names関数の型


def list_available_os_versions(
    memory: Memory,
    os: OS,
    image_names: Callback,
) -> list[OSVersion]:
    """利用可能なOSバージョンを取得."""
    mem_names = filter(memory.is_match, image_names())
    s = set(filter(os.is_match, mem_names))
    return sorted({os.version(n) for n in s}, key=operator.attrgetter("value"))


def find_available_os_latest_version(
    memory: Memory,
    os: OS,
    image_names: Callback,
) -> OSVersion:
    """利用可能な最新OSバージョンを取得."""
    vers = list_available_os_versions(memory, os, image_names)
    if len(vers) == 0:
        raise NotFoundOSVersionError
    return vers[-1]


def list_available_apps(
    memory: Memory,
    os: OS,
    os_version: OSVersion,
    image_names: Callback,
) -> list[Application]:
    """引数のOS,versionで利用可能なアプリ,バージョン一覧."""
    os_versions = list_available_os_versions(memory, os, image_names)
    if os_version.is_latest():
        os_version = find_available_os_latest_version(memory, os, image_names)
    if os_version not in os_versions:
        msg = (
            f"{os}のバージョン{os_version.value}は利用できません."
            f"利用可能なバージョンは{[v.value for v in os_versions]}です"
        )
        raise NotFoundOSVersionError(msg)
    mem_names = filter(memory.is_match, image_names())
    os_names = filter(os.is_match, mem_names)
    ver_names = filter(os_version.is_match, os_names)
    appsv = [os.app_with_version(n) for n in ver_names]
    return sorted(appsv, key=operator.attrgetter("name"))


def find_plan_id(memory: Memory) -> UUID:
    """メモリ容量からFlavor IDをみつける."""
    flavor = first_vmplan_by("name", memory.expression)
    if flavor is None:
        msg = f"{memory.value}GBのプランIDがみつかりませんでした"
        raise NotFoundFlavorIdError(msg)
    return flavor.flavor_id


def find_image_id(
    memory: Memory,
    os: OS,
    os_version: OSVersion,
    app: Application,
    list_images: Callable[[], list[Image]] = list_images,
) -> UUID:
    """指定条件からimage idを一意に検索する."""

    @cache
    def list_image_names() -> list[str]:
        """VM Image名一覧."""
        return [img.name for img in list_images()]

    if os_version.is_latest():
        os_version = find_available_os_latest_version(memory, os, list_image_names)
    if os_version not in list_available_os_versions(memory, os, list_image_names):
        raise NotFoundOSVersionError

    if app not in list_available_apps(memory, os, os_version, list_image_names):
        raise NotFoundApplicationError

    def pred(img: Image) -> bool:
        n = img.name

        return (
            memory.is_match(n)
            and os.is_match(n)
            and os_version.is_match(n)
            and app.is_match(n, os)
        )

    res = list(filter(pred, list_images()))
    if len(res) != 1:
        view(res, keys={}, style="table", pass_command=False)
        raise ImageIdMappingMismatchWarning

    return res[0].image_id


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
