"""VM add repo test."""
from __future__ import annotations

import itertools
import json
from functools import cache
from ipaddress import IPv4Address
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import pytest

from conoha_client.add_vm.domain.domain import Application
from conoha_client.add_vm.domain.errors import (
    NotFlavorProvidesError,
    NotFoundAddedVMError,
)
from conoha_client.features._shared.conftest import prepare
from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.image.domain import Image

from .domain import OS, Memory, OSVersion
from .repo import AddVMCommand, ImageInfoRepo, find_added

if TYPE_CHECKING:
    from requests_mock import Mocker


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
                "created": "2023-07-12T04:36:33Z",
                "minDisk": 30,
            },
        )
        for j in json.loads(p.read_text())
    ]


def test_list_available_os_versions() -> None:
    """Test for regression."""
    repo = ImageInfoRepo(
        memory=Memory.MG512,
        os=OS.UBUNTU,
        list_images=mock_list_images,
    )
    expected = [
        OSVersion(value=v, os=OS.UBUNTU) for v in ["16.04", "20.04", "20.04.2", "22.04"]
    ]
    assert repo.available_os_versions == expected

    repo2 = ImageInfoRepo(
        memory=Memory.GB64,
        os=OS.UBUNTU,
        list_images=mock_list_images,
    )
    expected2 = [
        OSVersion(value=v, os=OS.UBUNTU)
        for v in ["16.04", "18.04", "20.04", "20.04.2", "22.04"]
    ]
    assert repo2.available_os_versions == expected2


def test_find_available_os_latest() -> None:
    """Test for regression."""
    repo = ImageInfoRepo(
        memory=Memory.MG512,
        os=OS.UBUNTU,
        list_images=mock_list_images,
    )
    assert repo.available_os_latest_version == OSVersion(value="22.04", os=OS.UBUNTU)


def test_list_available_apps() -> None:
    """Test for regression."""
    v = OSVersion(value="9.2", os=OS.ALMA)
    repo = ImageInfoRepo(memory=Memory.MG512, os=OS.ALMA, list_images=mock_list_images)
    assert repo.list_available_apps(v) == [Application.none()]


def test_list_available_apps_by_latest() -> None:
    """Test for regression."""
    v = OSVersion(value="latest", os=OS.ALMA)
    repo = ImageInfoRepo(memory=Memory.MG512, os=OS.ALMA, list_images=mock_list_images)
    assert repo.list_available_apps(v) == [Application.none()]


def test_find_image_id() -> None:
    """一意にimage idを見つける. 一番大事."""
    cnt = 0
    imgids = set()
    for mem, _os in itertools.product(Memory, OS):
        repo = ImageInfoRepo(memory=mem, os=_os, list_images=mock_list_images)
        for os_v in repo.available_os_versions:
            for _app in repo.list_available_apps(os_v):
                im = repo.find_image_id(os_v, _app)
                imgids.add(im)
                cnt += 1

    # windowsの分を除外 -10
    # devを除外 -1
    assert len(imgids) == len(mock_list_images()) - 10 - 1


VM_ID = "d9302160-27f5-42f8-8993-d2735d2b0c24"


def test_add_vm() -> None:
    """VM追加."""

    def mock_post(_dummy: any) -> object:
        """add_vm mock."""
        return {
            "security_groups": [{"name": "default"}],
            "OS-DCF:diskConfig": "MANUAL",
            "id": VM_ID,
            "links": [
                {
                    "href": "https://compute.tyo3.conoha.io/v2/49756f55e53248df82e2e4cf080d6ceb/servers/d9302160-27f5-42f8-8993-d2735d2b0c24",
                    "rel": "self",
                },
                {
                    "href": "https://compute.tyo3.conoha.io/49756f55e53248df82e2e4cf080d6ceb/servers/d9302160-27f5-42f8-8993-d2735d2b0c24",
                    "rel": "bookmark",
                },
            ],
            "adminPass": "xxx",
        }

    cmd = AddVMCommand(
        flavor_id=uuid4(),
        image_id=uuid4(),
        admin_pass="xxx",  # noqa: S106
        sshkey_name=None,
        post=mock_post,
    )

    added = cmd()
    assert added.vm_id == UUID(VM_ID)


def test_invalid_add_vm(
    requests_mock: Mocker,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Invalid case."""
    prepare(requests_mock, monkeypatch)
    requests_mock.post(Endpoints.COMPUTE.tenant_id_url("servers"), status_code=400)

    cmd = AddVMCommand(
        flavor_id=uuid4(),
        image_id=uuid4(),
        admin_pass="xxx",  # noqa: S106
        sshkey_name=None,
    )
    with pytest.raises(NotFlavorProvidesError):
        cmd()


def test_find_ipv4() -> None:
    """Test."""
    expected = IPv4Address("157.7.78.59")  # fixutureのipv4

    def mock_get_servers() -> list[object]:
        """list_imageのモック."""
        p = Path(__file__).resolve().parent / "fixture_servers20231006.json"
        return json.loads(p.read_text())

    added = find_added(UUID(VM_ID), dep=mock_get_servers)
    assert added.ipv4 == expected


def test_invalid_find_ipv4() -> None:
    """Invalid case."""

    def mock_get_servers() -> list[object]:
        """2個目しか契約中VMが見つからない."""
        p = Path(__file__).resolve().parent / "fixture_servers20231006.json"
        return [json.loads(p.read_text())[1]]

    with pytest.raises(NotFoundAddedVMError):
        find_added(UUID(VM_ID), dep=mock_get_servers)
