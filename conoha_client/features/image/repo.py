"""VM Image API."""
from __future__ import annotations

from functools import cache

from conoha_client.features import Endpoints

from .domain import Image


@cache
def list_images() -> list[Image]:
    """イメージ一覧を取得する."""
    res = Endpoints.COMPUTE.get("images/detail").json()
    return [Image.model_validate(e) for e in res["images"]]


# dist指定でバージョン一覧を取得
# human friendlyな指定でimage id を探せるようにしたい
