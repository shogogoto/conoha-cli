"""VM add repo test."""
from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from conoha_client.features.image.domain import (
    Application,
    Distribution,
    DistVersion,
)
from conoha_client.features.image.domain.test_domain import fixture_models
from conoha_client.features.plan.domain import Memory

from .repo import (
    DistQuery,
)

if TYPE_CHECKING:
    from conoha_client.features.image.domain import Image
    from conoha_client.features.image.domain.image import LinuxImageList


def mock_list_images() -> list[Image]:
    """list_imageのモック."""
    return fixture_models().root


def mock_dep() -> LinuxImageList:
    """list_imageのモック."""
    return fixture_models().priors.linux


def q(mem: Memory, dist: Distribution) -> DistQuery:
    """Test util."""
    return DistQuery(
        memory=mem,
        dist=dist,
        dep=mock_dep,
    )


def test_list_available_dist_versions() -> None:
    """Test for regression."""
    q1 = q(Memory.MB512, Distribution.UBUNTU)
    assert q1.available_vers() == {
        DistVersion(value=v) for v in ["16.04", "20.04", "20.04.2", "22.04"]
    }

    q2 = q(Memory.GB64, Distribution.UBUNTU)
    assert q2.available_vers() == {
        DistVersion(value=v) for v in ["16.04", "18.04", "20.04", "20.04.2", "22.04"]
    }


def test_dist_latest_version() -> None:
    """Test for regression."""
    q1 = q(Memory.MB512, Distribution.UBUNTU)
    assert q1.latest_ver() == DistVersion(value="22.04")

    q2 = q(Memory.MB512, Distribution.ALMA)
    assert q2.latest_ver() == DistVersion(value="9.2")


def test_list_available_apps() -> None:
    """Test for regression."""
    alma_latest = DistVersion(value="9.2")
    q1 = q(Memory.MB512, Distribution.ALMA)
    assert q1.apps(alma_latest) == {Application.null()}


def test_find_image_id() -> None:
    """一意にimage idを見つける. 一番大事."""
    n_all = len(mock_dep())
    imgs = set()
    for mem, dist in itertools.product(Memory, Distribution):
        q_ = q(mem, dist)
        for v in q_.available_vers():
            for app in q_.apps(v):
                img = q_.identify(v, app)
                imgs.add(img)

    # freebsdのufsの30gb,100gbを無視した
    assert len(imgs) == n_all - 2
