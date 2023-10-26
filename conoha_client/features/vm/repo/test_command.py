"""command tests."""
from __future__ import annotations

import json
from ipaddress import IPv4Address
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import pytest

from conoha_client.features._shared.conftest import prepare
from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.vm.errors import (
    NotFlavorProvidesError,
    NotFoundAddedVMError,
)
from conoha_client.features.vm.repo.command import AddVMCommand, find_added

if TYPE_CHECKING:
    from requests_mock import Mocker

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
