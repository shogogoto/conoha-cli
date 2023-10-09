"""VM actions Repository tests."""


from uuid import uuid4

import pytest
from requests_mock import Mocker

from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.vm_actions.domain.errors import VMDeleteError

from .repo import remove_vm


def test_invalid_remove_vm(requests_mock: Mocker) -> None:
    """Invalid case."""
    requests_mock.post(
        Endpoints.IDENTITY.url("tokens"),
        json={"access": {"token": {"id": "test_token"}}},
    )
    uid = uuid4()
    requests_mock.delete(
        Endpoints.COMPUTE.tenant_id_url(f"servers/{uid}"),
        status_code=404,
    )
    with pytest.raises(VMDeleteError):
        remove_vm(uid)
