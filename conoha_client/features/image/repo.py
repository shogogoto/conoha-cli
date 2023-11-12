"""VM Image API."""
from __future__ import annotations

from http import HTTPStatus

from conoha_client.features import Endpoints
from conoha_client.features.image.domain.errors import (
    DeleteImageError,
    DeletePriorImageForbiddenError,
)

from .domain import Image, ImageList


def list_images() -> ImageList:
    """イメージ一覧を取得する."""
    res = Endpoints.COMPUTE.get("images/detail").json()
    return ImageList([Image.model_validate(e) for e in res["images"]])


def remove_image(image: Image) -> None:
    """イメージを削除."""
    res = Endpoints.IMAGE.delete(f"images/{image.image_id}")
    if res.status_code == HTTPStatus.FORBIDDEN:
        msg = f"所与のイメージ{image.name}は削除できません"
        raise DeletePriorImageForbiddenError(msg)
    if res.status_code != HTTPStatus.NO_CONTENT:
        raise DeleteImageError
