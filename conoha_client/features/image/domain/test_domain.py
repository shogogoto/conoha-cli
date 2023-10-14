"""Image domain test."""
from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from uuid import uuid4

import pytest

from conoha_client.features.image.domain.operating_system import Distribution

from .errors import NeitherWindowsNorLinuxError, NotLinuxError
from .image import Image, ImageList


@cache
def fixture_models() -> ImageList:
    """All names."""
    p = Path(__file__).resolve().parent / "fixture20231014.json"

    ls = [
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
    return ImageList(ls)


def test_valid_os() -> None:
    """OS名が含まれているか."""
    fixture_models()


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


def test_get_snapshots() -> None:
    """ユーザーが保存したVMイメージを取得する."""
    ls = fixture_models().snapshots
    assert ls.root[0].name == "dev"


def test_distribution() -> None:
    """Linux distを網羅できている."""
    for m in fixture_models().priors.linux:
        assert Distribution.create(m) in Distribution

    for m in fixture_models().priors.windows:
        with pytest.raises(NotLinuxError):
            Distribution.create(m)


def test_distribution_versions() -> None:
    """ubuntuのみ確認. ついでにdebian."""
    lins = fixture_models().priors.linux
    u_vers = lins.dist_versions(Distribution.UBUNTU)
    assert u_vers == {"16.04", "18.04", "20.04", "20.04.2", "22.04"}
    d_vers = lins.dist_versions(Distribution.DEBIAN)
    assert d_vers == {"10.10", "11.0", "12.0"}


def test_dist_applications() -> None:
    """ubuntuのみ確認."""
    # lins = models().priors.linux
    # apps1 = lins.applications(Distribution.UBUNTU, "16.04")
    # print(apps1)

    # apps2 = lins.applications(Distribution.UBUNTU, "18.04")
    # print(apps2)

    # apps3 = lins.applications(Distribution.UBUNTU, "20.04")
    # print(apps3)

    # apps4 = lins.applications(Distribution.UBUNTU, "20.04.2")
    # print(apps4)

    # apps5 = lins.applications(Distribution.UBUNTU, "22.04")
    # print(apps5)
