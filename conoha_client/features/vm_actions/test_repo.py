"""VM actions Repository tests."""


from uuid import uuid4

import pytest
from requests_mock import Mocker

from conoha_client.features._shared.conftest import prepare
from conoha_client.features._shared.endpoints.endpoints import Endpoints
from conoha_client.features.vm_actions.domain.errors import VMDeleteError

from .repo import remove_vm


def test_invalid_remove_vm(
    requests_mock: Mocker,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Invalid case."""
    prepare(requests_mock, monkeypatch)
    uid = uuid4()
    requests_mock.delete(
        Endpoints.COMPUTE.tenant_id_url(f"servers/{uid}"),
        status_code=404,
    )
    with pytest.raises(VMDeleteError):
        remove_vm(uid)
