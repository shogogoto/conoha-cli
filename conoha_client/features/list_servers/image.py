"""イメージ一覧取得."""
from __future__ import annotations

from functools import cache
from uuid import UUID

from pydantic import BaseModel

from conoha_client.features.share import Endpoints


class Image(BaseModel, frozen=True):
    """VPSイメージ.

    :param image_id: イメージID
    :param app: アプリケーション名
    :param os: OSタイプ
    """

    image_id: UUID
    app: str|None
    os: str

    @classmethod
    def parse(cls, one: dict)-> Image:
        """HTTPレスポンスからイメージ情報へ変換.

        :param one: json["images"]: list[dict]の要素
        """
        meta = one["metadata"]
        return Image(
            image_id=UUID(one["id"]),
            app=meta.get("app"),
            os=meta["os_type"],
        )


@cache
def list_images() -> list[Image]:
    """イメージ一覧を取得する."""
    res = Endpoints.COMPUTE.get("images/detail").json()
    return [Image.parse(e) for e in res["images"]]


def search_image(image_id: UUID) -> Image:
    """IDからイメージを返す.

    :param image_id: フレーバーID
    """
    def pred(e:Image) -> bool:
        return e.image_id == image_id

    result = filter(pred, list_images())
    return next(result)
