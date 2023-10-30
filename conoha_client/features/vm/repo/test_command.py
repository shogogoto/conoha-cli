"""command tests."""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import pytest

from conoha_client.features._shared.conftest import prepare
from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.vm.errors import (
    VMMemoryShortageError,
)
from conoha_client.features.vm.repo.command import AddVMCommand

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
        dep=mock_post,
    )

    added = cmd(None)
    assert added.vm_id == UUID(VM_ID)


def test_invalid_add_vm(
    requests_mock: Mocker,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Invalid case error code 400. 課金に関わるから慎重."""
    prepare(requests_mock, monkeypatch)
    requests_mock.post(
        Endpoints.COMPUTE.tenant_id_url("servers"),
        status_code=400,
        json={
            "badRequest": {
                "message": "Flavor's disk is too small for requested image.",
            },
        },
    )

    cmd = AddVMCommand(
        flavor_id=uuid4(),
        image_id=uuid4(),
        admin_pass="xxx",  # noqa: S106
    )
    with pytest.raises(VMMemoryShortageError):
        cmd(None)
