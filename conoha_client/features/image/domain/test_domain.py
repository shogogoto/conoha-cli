"""add VM domain test."""
from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from uuid import uuid4

import pytest

from conoha_client.features.image.domain.errors import NeitherWindowsNorLinuxError
from conoha_client.features.image.domain.image import Image


@cache
def models() -> list[Image]:
    """All names."""
    p = Path(__file__).resolve().parent.parent / "fixture20231014.json"

    return [
        Image.model_validate(
            {
                "id": j["image_id"],
                "name": j["name"],
                "metadata": {
                    "dst": j["dist"],
                    "app": j["app"],
                    "os_type": j["os"],
                    "image_type": j.get("image_type"),
                },
                "created": j["created"],
                "minDisk": j["minDisk"],
            },
        )
        for j in json.loads(p.read_text())
    ]


def test_valid_os() -> None:
    """OS名が含まれているか."""
    models()


def test_invalid_os() -> None:
    """Windows, Linux以外のOS."""
    with pytest.raises(NeitherWindowsNorLinuxError):
        Image.model_validate(
            {
                "id": str(uuid4()),
                "name": "dummy",
                "metadata": {
                    "dst": "dummy",
                    "app": "dummy",
                    "os_type": "neither_win_nor_lin",
                },
                "created": "2023-09-27T14:22:50+09:00",
                "minDisk": 30,
            },
        )


# def test_invalid_get_os() -> None:
#     """OS名が含まれているか."""
#     with pytest.raises(OSIdentificationError):
#         ImageName("xxx-unknown_os-yyy").os


# def test_get_os_version() -> None:
#     """OS Versionを取得できるか."""
#     for n in names():
#         name = ImageName(n)
#         print(n, name.os_version)


# def test_get_win_version() -> None:
#     """Windowsの場合は後ろ2要素を結合したものがバージョンとなる."""
#     n1 = ImageName("vmi-win2019dce-rds")
#     assert n1.os_version == Version("2019dce")

# assert n1.os_version == OSVersion(
#     value="win2019dce-rds",
#     os=OS.WINDOWS,
# )
# assert OS.WINDOWS.version("vmi-win-2019dce-amd64") == OSVersion(
#     value="win-2019dce",
#     os=OS.WINDOWS,
# )


# def test_invalid_get_os_version() -> None:
#     """OS Versionが取得できないときに適切なエラーが出るか."""
#     with pytest.raises(OSVersionExtractError):
#         OS.UBUNTU.version("xxx-ubun-22.0")
#     with pytest.raises(OSVersionExtractError):
#         OS.UBUNTU.version("xxx-ubuntu")


# def test_get_app_with_version() -> None:
#     """OSに紐づいたアプリ名とバージョンを取得する."""
#     av1 = OS.UBUNTU.app_with_version("vmi-rust-latest-ubuntu-20.04-amd64-100gb")
#     assert av1 == Application(name="rust", version="latest")
#     av3 = OS.DEBIAN.app_with_version("vmi-debian-12.0-amd64-100gb")
#     assert av3 == Application.none()
#     av4 = OS.CENTOS.app_with_version(
#         "vmi-cacti-nagios-1.2.17.4.4.6-centos-7.9-amd64-30gb",
#     )

#     assert av4 == Application(
#         name="cacti-nagios",
#         version="1.2.17.4.4.6",
#     )


# def test_invalid_get_app_with_version() -> None:
#     """OSに紐づいたアプリ名とバージョンを取得に失敗する."""
#     with pytest.raises(OSVersionExtractError):
#         OS.UBUNTU.app_with_version("dev")

#     with pytest.raises(ApplicationWithoutVersionError):
#         OS.UBUNTU.app_with_version(
#             "vmi-appname_without_version-ubuntu-20.02-amd64-100gb",
#         )
