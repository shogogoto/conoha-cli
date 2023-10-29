"""VM Image API."""
from __future__ import annotations

from functools import cache
from http import HTTPStatus

from conoha_client.features import Endpoints
from conoha_client.features.image.domain.errors import (
    DeleteImageError,
    DeletePriorImageForbiddenError,
)

from .domain import Image, ImageList


@cache
def list_images() -> ImageList:
    """イメージ一覧を取得する."""
    res = Endpoints.COMPUTE.get("images/detail").json()
    return ImageList([Image.model_validate(e) for e in res["images"]])


# def find_image_by_starts_with(
#     starts: str,
#     attr: str,
#     dep: Callable[[], ImageList] = list_images,
# ) -> Image:
#     """前方一致で検索."""

#     def pred(img: Image) -> bool:
#         val = getattr(img, attr)
#         return str(val).startswith(starts)

#     ls = [img for img in dep().root if pred(img)]
#     n = len(ls)
#     if n != 1:
#         msg = f"「{starts}」で前方一致検索で{n}件がヒットしました"
#         raise ImageIdMatchNotUniqueError(msg)
#     return ls[0]


def remove_snapshot(image: Image) -> None:
    """イメージを削除."""
    res = Endpoints.IMAGE.delete(f"images/{image.image_id}")
    if res.status_code == HTTPStatus.FORBIDDEN:
        msg = f"所与のイメージ{image.name}は削除できません"
        raise DeletePriorImageForbiddenError(msg)
    if res.status_code != HTTPStatus.NO_CONTENT:
        raise DeleteImageError
