import pytest
from requests_mock import Mocker

from .endpoints import Endpoints


def prepare(
    requests_mock: Mocker,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """requestsを含むテストケースの準備."""
    monkeypatch.setenv("OS_CONOHA_REGION_NO", "1")
    monkeypatch.setenv("OS_TENANT_ID", "tenant-id")
    monkeypatch.setenv("OS_USERNAME", "testuser")
    monkeypatch.setenv("OS_PASSWORD", "testuser")

    requests_mock.post(
        Endpoints.IDENTITY.url("tokens"),
        json={"access": {"token": {"id": "test_token"}}},
    )
