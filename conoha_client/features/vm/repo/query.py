"""契約中VM API."""
from __future__ import annotations

from typing import Callable

from conoha_client.features._shared import Endpoints
from conoha_client.features.vm.domain import VM


def get_dep() -> list[object]:
    """For Dependency Injection."""
    res = Endpoints.COMPUTE.get("servers/detail").json()
    return res["servers"]


def list_servers(
    dep: Callable[[], list[object]] = get_dep,
) -> list[VM]:
    """契約中のサーバー情報一覧を取得する."""
    res = dep()
    return [VM.model_validate(e) for e in res]
