"""VM Create API."""
from __future__ import annotations

from typing import Callable
from uuid import UUID

from conoha_client.features.image.repo import list_images
from conoha_client.features.plan import find_vmplan_by

from .domain import OS, ImageNames, Memory, NotFoundFlavorIdError, Version
from .domain.errors import NotFoundVersionError


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


# def list_available_apps(
#     memory: Memory,
#     os: OS,
#     os_version: Version,
# ):
#     """引数のOS,versionで利用可能なアプリ,バージョン一覧."""
#     all_names = [img.name for img in list_images()]
#     mem_names = filter(memory.is_match, all_names)
#     print(list(mem_names))
#     os_names = filter(os.is_match, mem_names)
#     print(os)
#     print(os)
#     print(os)
#     print(os)
#     print(list(os_names))
#     ver_names = filter(os_version.is_match, os_names)
#     names = ImageNames(values=list(ver_names))
#     print(names)
#     print(names)
#     print(names)
#     print(names)
#     return names.available_apps(os)
#     # vers = list_available_os_versions(memory, os)
#     # print(vers)
#     # os.app_with_version()
#     # pass


# def add_vm(mem: Memory, os: OS, app: str) -> None:
#     """新規VM追加."""
#     find_vmplan_by("name", mem.expression)
#     # def pred(img: Image) -> bool:
#     #     in_os = os_.value in img.name
#     #     in_app = app.value in img.app
#     #     return in_os and in_app

#     # image = filter_model_by(list_images(), pred)
#     # print(image)
#     # js = {"flavorRef": plan.flavor_id, "imageRef": image.image_id}
#     # print(js)
#     # Endpoints.COMPUTE.post("servers", json=js)
