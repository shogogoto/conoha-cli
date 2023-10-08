"""契約中VM API."""
from __future__ import annotations

from typing import Callable

from conoha_client.features._shared import Endpoints

from .domain import Server


def get_dep() -> list[object]:
    """For Dependency Injection."""
    res = Endpoints.COMPUTE.get("servers/detail").json()
    return res["servers"]


def list_servers(
    get: Callable[[], list[object]] = get_dep,
) -> list[Server]:
    """契約中のサーバー情報一覧を取得する."""
    res = get()
    return [Server.model_validate(e) for e in res]
