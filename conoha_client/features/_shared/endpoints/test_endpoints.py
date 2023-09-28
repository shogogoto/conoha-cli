"""test endpoints."""


from _pytest.monkeypatch import MonkeyPatch

from .endpoints import Endpoints


def test_url(monkeypatch: MonkeyPatch) -> None:
    """tenant_idなしurl."""
    tid = "tenant-id"
    monkeypatch.setenv("OS_CONOHA_REGION_NO", "1")
    monkeypatch.setenv("OS_TENANT_ID", tid)

    relative = "xxx"
    url = Endpoints.ACCOUNT.url(relative)
    if tid in url:
        msg = "Expected without tenant id"
        raise ValueError(msg)

    if relative not in url:
        msg = "Expected with relative"
        raise ValueError(msg)


def test_tenant_id_url(monkeypatch: MonkeyPatch) -> None:
    """tenant_id有りurl."""
    tid = "tenant-id"
    monkeypatch.setenv("OS_CONOHA_REGION_NO", "1")
    monkeypatch.setenv("OS_TENANT_ID", tid)

    relative = "xxx"
    url = Endpoints.ACCOUNT.tenant_id_url(relative)
    if tid not in url:
        msg = "Expected with tenant id"
        raise ValueError(msg)

    if relative not in url:
        msg = "Expected with relative"
        raise ValueError(msg)
