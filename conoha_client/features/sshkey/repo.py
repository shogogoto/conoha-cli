"""sshkey API Repository."""
from __future__ import annotations

from http import HTTPStatus

from conoha_client.features._shared import Endpoints

from .domain import KeyPair, KeyPairAlreadyExistsError, KeyPairNotFoundError


def find_all() -> list[KeyPair]:
    """sshキー一覧取得."""
    res = Endpoints.COMPUTE.get("os-keypairs").json()["keypairs"]
    return [KeyPair.model_validate(d["keypair"]) for d in res]


def create_keypair() -> KeyPair:
    """sshキーペアを新規作成.

    APIは以下を返す
    [{
        "public_key": "ssh-rsa ",
        "private_key": "...",
        "user_id": "...",
        "name": "conoha-client-2023-09-28-14-04",
        "fingerprint": "xx:xx:...":
    }]
    """
    name = KeyPair.publish_name()
    body = {"keypair": {"name": name}}
    res = Endpoints.COMPUTE.post("os-keypairs", json=body)
    if res.status_code == HTTPStatus.CONFLICT:
        msg = f"{name}は既に存在します"
        raise KeyPairAlreadyExistsError(msg)

    return KeyPair.model_validate(res.json()["keypair"])


def remove_keypair(name: str) -> None:
    """sshキー削除.

    :param name: 削除したいキーペア名
    """
    res = Endpoints.COMPUTE.delete(f"os-keypairs/{name}")
    if res.status_code == HTTPStatus.NOT_FOUND:
        msg = f"{name}キーペアが存在しないため、削除できませんでした"
        raise KeyPairNotFoundError(msg)
