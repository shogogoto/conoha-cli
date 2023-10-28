"""VM Image API."""
from __future__ import annotations

from functools import cache

from conoha_client.features import Endpoints
from conoha_client.features.image.domain.image import ImageList

from .domain import Image


@cache
def list_images() -> ImageList:
    """イメージ一覧を取得する."""
    res = Endpoints.COMPUTE.get("images/detail").json()
    return ImageList([Image.model_validate(e) for e in res["images"]])
