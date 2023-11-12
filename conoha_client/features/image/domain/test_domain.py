"""Image domain test."""
from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from uuid import uuid4

import pytest

from conoha_client.features._shared.util import now_jst

from .distribution import (
    Distribution,
    DistVersion,
)
from .errors import NeitherWindowsNorLinuxError, NotLinuxError
from .image import Image, ImageList


@cache
def fixture_models() -> ImageList:
    """fixture."""
    p = Path(__file__).resolve().parent / "fixture20231014.json"

    dummy = now_jst()
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
                "updated": dummy,
                "minDisk": j["minDisk"],
                "progress": 100,
                "OS-EXT-IMG-SIZE:size": 999,
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
                "progress": 100,
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
    assert u_vers == {
        DistVersion(value=v) for v in ["16.04", "18.04", "20.04", "20.04.2", "22.04"]
    }
    d_vers = lins.dist_versions(Distribution.DEBIAN)
    assert d_vers == {DistVersion(value=v) for v in ["10.10", "11.0", "12.0"]}
