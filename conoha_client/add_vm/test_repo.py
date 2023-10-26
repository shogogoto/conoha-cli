"""VM add repo test."""
from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from conoha_client.features.image.domain.operating_system import Distribution
from conoha_client.features.image.domain.test_domain import fixture_models
from conoha_client.features.plan.domain import Memory

from .repo import (
    DistoQuery,
    available_apps,
    available_dist_latest_version,
    available_dist_versions,
    identify_image,
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


def test_list_available_dist_versions() -> None:
    """Test for regression."""
    q1 = DistoQuery(
        memory=Memory.MB512,
        disto=Distribution.UBUNTU,
        dep=mock_dep,
    )
    assert q1.available_vers() == {"16.04", "20.04", "20.04.2", "22.04"}

    q2 = DistoQuery(
        memory=Memory.GB64,
        disto=Distribution.UBUNTU,
        dep=mock_dep,
    )
    assert q2.available_vers() == {"16.04", "18.04", "20.04", "20.04.2", "22.04"}


def test_dist_latest_version() -> None:
    """Test for regression."""
    actual1 = available_dist_latest_version(
        memory=Memory.MB512,
        dist=Distribution.UBUNTU,
        dep=mock_dep,
    )
    assert actual1 == "22.04"

    actual2 = available_dist_latest_version(
        memory=Memory.MB512,
        dist=Distribution.ALMA,
        dep=mock_dep,
    )
    assert actual2 == "9.2"


def test_list_available_apps() -> None:
    """Test for regression."""
    alma_latest = "9.2"
    actual = available_apps(
        Memory.MB512,
        Distribution.ALMA,
        alma_latest,
        dep=mock_dep,
    )
    assert actual == {""}


def test_find_image_id() -> None:
    """一意にimage idを見つける. 一番大事."""
    n_all = len(mock_dep())
    imgs = set()
    for mem, disto in itertools.product(Memory, Distribution):
        vers = available_dist_versions(
            memory=mem,
            dist=disto,
            dep=mock_dep,
        )
        for v in vers:
            apps = available_apps(mem, disto, v, dep=mock_dep)
            for app in apps:
                img = identify_image(mem, disto, v, app, dep=mock_dep)
                imgs.add(img)
    # freebsdのufs 30gb, 100gbを無視した
    assert len(imgs) == n_all - 2


# VM_ID = "d9302160-27f5-42f8-8993-d2735d2b0c24"


# def test_add_vm() -> None:
#     """VM追加."""

#     def mock_post(_dummy: any) -> object:
#         """add_vm mock."""
#         return {
#             "security_groups": [{"name": "default"}],
#             "OS-DCF:diskConfig": "MANUAL",
#             "id": VM_ID,
#             "links": [
#                 {
#                     "href": "https://compute.tyo3.conoha.io/v2/49756f55e53248df82e2e4cf080d6ceb/servers/d9302160-27f5-42f8-8993-d2735d2b0c24",
#                     "rel": "self",
#                 },
#                 {
#                     "href": "https://compute.tyo3.conoha.io/49756f55e53248df82e2e4cf080d6ceb/servers/d9302160-27f5-42f8-8993-d2735d2b0c24",
#                     "rel": "bookmark",
#                 },
#             ],
#             "adminPass": "xxx",
#         }

#     cmd = AddVMCommand(
#         flavor_id=uuid4(),
#         image_id=uuid4(),
#         admin_pass="xxx",
#         sshkey_name=None,
#         post=mock_post,
#     )

#     added = cmd()
#     assert added.vm_id == UUID(VM_ID)


# def test_invalid_add_vm(
#     requests_mock: Mocker,
#     monkeypatch: pytest.MonkeyPatch,
# ) -> None:
#     """Invalid case."""
#     prepare(requests_mock, monkeypatch)
#     requests_mock.post(Endpoints.COMPUTE.tenant_id_url("servers"), status_code=400)

#     cmd = AddVMCommand(
#         flavor_id=uuid4(),
#         image_id=uuid4(),
#         admin_pass="xxx",
#         sshkey_name=None,
#     )
#     with pytest.raises(NotFlavorProvidesError):
#         cmd()


# def test_find_ipv4() -> None:
#     """Test."""
#     expected = IPv4Address("157.7.78.59")  # fixutureのipv4

#     def mock_get_servers() -> list[object]:
#         """list_imageのモック."""
#         p = Path(__file__).resolve().parent / "fixture_servers20231006.json"
#         return json.loads(p.read_text())

#     added = find_added(UUID(VM_ID), dep=mock_get_servers)
#     assert added.ipv4 == expected


# def test_invalid_find_ipv4() -> None:
#     """Invalid case."""

#     def mock_get_servers() -> list[object]:
#         """2個目しか契約中VMが見つからない."""
#         p = Path(__file__).resolve().parent / "fixture_servers20231006.json"
#         return [json.loads(p.read_text())[1]]

#     with pytest.raises(NotFoundAddedVMError):
#         find_added(UUID(VM_ID), dep=mock_get_servers)
