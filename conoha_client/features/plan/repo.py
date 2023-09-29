"""VM Plan. API."""
from __future__ import annotations

from functools import cache

from conoha_client.features.add_vm.repo import Endpoints

from .domain import Flavor


@cache
def list_flavors() -> list[Flavor]:
    """MVプラン一覧を取得する."""
    res = Endpoints.COMPUTE.get("flavors/detail").json()
    return [Flavor.model_validate(e) for e in res["flavors"]]


def find_id_by(attr_name: str, value: any) -> list[Flavor]:
    """key-valueにマッチしたプラン情報を返す."""

    def pred(e: Flavor) -> bool:
        return str(getattr(e, attr_name)) == value

    return list(filter(pred, list_flavors()))
