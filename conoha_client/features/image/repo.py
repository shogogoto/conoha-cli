"""VM Image API."""
from __future__ import annotations

from functools import cache

from conoha_client.features import Endpoints
from conoha_client.features._shared.domain import find_by_included_prop

from .domain import Image


@cache
def list_images() -> list[Image]:
    """イメージ一覧を取得する."""
    res = Endpoints.COMPUTE.get("images/detail").json()
    return [Image.model_validate(e) for e in res["images"]]


def find_image_by(attr_name: str, value: any) -> Image | None:
    """key-valueにマッチしたプラン情報を返す."""
    return find_by_included_prop(list_images(), attr_name, value)
