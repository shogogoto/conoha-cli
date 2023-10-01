"""VM Create API."""
from __future__ import annotations

import operator
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from conoha_client.add_vm.domain.domain import ImageNames
from conoha_client.features.image.repo import list_images
from conoha_client.features.plan import find_vmplan_by

from .domain import OS, Memory, NotFoundFlavorIdError, Version
from .domain.errors import NotFoundVersionError

if TYPE_CHECKING:
    from conoha_client.add_vm.domain.domain import Application


def find_plan_id(mem: Memory) -> UUID:
    """メモリ容量からFlavor IDをみつける."""
    flavor = find_vmplan_by("name", mem.expression)
    if flavor is None:
        msg = f"{mem.value}GBのプランIDがみつかりませんでした"
        raise NotFoundFlavorIdError(msg)
    return flavor.flavor_id


def list_image_names() -> list[str]:
    """VM Image名一覧."""
    return [img.name for img in list_images()]


Callback = Callable[[], list[str]]  # list_image_names関数の型


def list_available_os_versions(
    memory: Memory,
    os: OS,
    image_names: Callback,
) -> list[Version]:
    """利用可能なOSバージョンを取得."""
    mem_names = filter(memory.is_match, image_names())
    names = ImageNames(values=list(mem_names))
    return names.available_os_versions(os)


def find_available_os_latest_version(
    memory: Memory,
    os: OS,
    image_names: Callback,
) -> Version:
    """利用可能な最新OSバージョンを取得."""
    vers = list_available_os_versions(memory, os, image_names)
    if len(vers) == 0:
        raise NotFoundVersionError
    return vers[-1]


def list_available_apps(
    memory: Memory,
    os: OS,
    os_version: Version,
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
        raise NotFoundVersionError(msg)
    mem_names = filter(memory.is_match, image_names())
    os_names = filter(os.is_match, mem_names)
    ver_names = filter(os_version.is_match, os_names)
    appsv = [os.app_with_version(n) for n in ver_names]
    return sorted(appsv, key=operator.attrgetter("name"))


def add_vm(mem: Memory, os: OS, app: Application) -> None:
    """新規VM追加."""
    print(mem, os, app)  # noqa: T201
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
