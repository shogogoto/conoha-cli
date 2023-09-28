"""sshkey API Repository."""
from __future__ import annotations

from conoha_client.features._shared import Endpoints

from .domain import KeyPair


def find_all() -> list[KeyPair]:
    """sshキー一覧取得."""
    res = Endpoints.COMPUTE.get("os-keypairs").json()["keypairs"]
    return [KeyPair.model_validate(d["keypair"]) for d in res]
