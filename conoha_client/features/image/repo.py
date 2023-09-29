"""VM Image API."""
from __future__ import annotations

from functools import cache

from conoha_client.features.add_vm.repo import Endpoints

from .domain import Image


@cache
def list_images() -> list[Image]:
    """イメージ一覧を取得する."""
    res = Endpoints.COMPUTE.get("images/detail").json()
    return [Image.model_validate(e) for e in res["images"]]


def find_id_by(attr_name: str, value: any) -> list[Image]:
    """key-valueにマッチしたプラン情報を返す."""

    def pred(e: Image) -> bool:
        return value in str(getattr(e, attr_name))

    return list(filter(pred, list_images()))
