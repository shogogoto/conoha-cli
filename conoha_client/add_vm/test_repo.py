"""VM add repo test."""
from __future__ import annotations

import itertools
import json
from functools import cache
from pathlib import Path

from conoha_client.add_vm.domain.domain import Application
from conoha_client.features.image.domain import Image

from .domain import OS, Memory, OSVersion
from .repo import ImageInfoRepo


@cache
def mock_list_images() -> list[Image]:
    """list_imageのモック."""
    p = Path(__file__).resolve().parent / "fixture20231002.json"
    return [
        Image.model_validate(
            {
                "id": j["image_id"],
                "name": j["name"],
                "metadata": {
                    "dst": j["dist"],
                    "app": j["app"],
                    "os_type": j["os"],
                },
            },
        )
        for j in json.loads(p.read_text())
    ]


def test_list_available_os_versions() -> None:
    """Test for regression."""
    repo = ImageInfoRepo(memory=Memory.MG512, os=OS.UBUNTU, list_image=mock_list_images)
    expected = [
        OSVersion(value=v, os=OS.UBUNTU) for v in ["16.04", "20.04", "20.04.2", "22.04"]
    ]
    assert repo.available_os_versions == expected

    repo2 = ImageInfoRepo(memory=Memory.GB64, os=OS.UBUNTU, list_image=mock_list_images)
    expected2 = [
        OSVersion(value=v, os=OS.UBUNTU)
        for v in ["16.04", "18.04", "20.04", "20.04.2", "22.04"]
    ]
    assert repo2.available_os_versions == expected2


def test_find_available_os_latest() -> None:
    """Test for regression."""
    repo = ImageInfoRepo(memory=Memory.MG512, os=OS.UBUNTU, list_image=mock_list_images)
    assert repo.available_os_latest_version == OSVersion(value="22.04", os=OS.UBUNTU)


def test_list_available_apps() -> None:
    """Test for regression."""
    v = OSVersion(value="9.2", os=OS.ALMA)
    repo = ImageInfoRepo(memory=Memory.MG512, os=OS.ALMA, list_image=mock_list_images)
    assert repo.list_available_apps(v) == [Application.none()]


def test_list_available_apps_by_latest() -> None:
    """Test for regression."""
    v = OSVersion(value="latest", os=OS.ALMA)
    repo = ImageInfoRepo(memory=Memory.MG512, os=OS.ALMA, list_image=mock_list_images)
    assert repo.list_available_apps(v) == [Application.none()]


def test_find_image_id() -> None:
    """一意にimage idを見つける. 一番大事."""
    cnt = 0
    imgids = set()
    for mem, _os in itertools.product(Memory, OS):
        repo = ImageInfoRepo(memory=mem, os=_os, list_image=mock_list_images)
        for os_v in repo.available_os_versions:
            for _app in repo.list_available_apps(os_v):
                im = repo.find_image_id(os_v, _app)
                imgids.add(im)
                cnt += 1

    # windowsの分を除外 -10
    # devを除外 -1
    assert len(imgids) == len(mock_list_images()) - 10 - 1
