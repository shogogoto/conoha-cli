"""契約中VM API."""
from __future__ import annotations

from conoha_client.features._shared import Endpoints

from .domain import Server


def list_servers() -> list[Server]:
    """契約中のサーバー情報一覧を取得する."""
    res = Endpoints.COMPUTE.get("servers/detail").json()
    return [Server.model_validate(e) for e in res["servers"]]
