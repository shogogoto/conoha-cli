"""Conoha APIのサービス一覧."""
from __future__ import annotations

from enum import Enum
from urllib.parse import urljoin

import requests

from .environments import env_region, env_tenant_id
from .token import token_headers

TIMEOUT = 3.0


class Endpoints(Enum):
    """Conoha APIのエンドポイントとバージョン情報のペア.

    ref: https://www.conoha.jp/docs/?btn_id=docs--sidebar_docs
    """

    ACCOUNT = ("account", "v1")
    COMPUTE = ("compute", "v2")
    VOLUME = ("block.storage", "v2")
    DATABASE = ("database-hosting", "v1")
    IMAGE = ("image-service", "v2")
    DNS = ("dns-service", "v1.0")
    STORAGE = ("object-storage", "v1")
    IDENTITY = ("identity", "v2.0")
    NETWORK = ("networking", "v2.0")

    def __init__(self, prefix: str, version: str) -> None:
        """Enumのプロパティ設定."""
        self.prefix = prefix
        self.version = version

    def url(self, relative: str) -> str:
        """エンドポイントを組み立てる.

        :param relative: baseURL以降の文字列
        """
        p = self.prefix
        r = env_region()
        v = self.version
        base = f"https://{p}.{r}.conoha.io/{v}/"
        return urljoin(base, relative)

    def tenant_id_url(self, relative: str) -> str:
        """Tenant id付きエンドポイントを組み立てる.

        :param relative: baseURL以降の文字列
        """
        url = self.url(env_tenant_id())
        return urljoin(f"{url}/", relative)

    def get(
        self,
        relative: str,
        params: dict | None = None,
    ) -> requests.Response:
        """HTTP GETリクエスト.

        :param relative: テナントID以降の文字列
        :param params: (optional) クエリパラメータ
        """
        url = self.tenant_id_url(relative)
        return requests.get(
            url,
            headers=token_headers(),
            timeout=TIMEOUT,
            params=params,
        )

    def post(self, relative: str, json: object) -> requests.Response:
        """HTTP POSTリクエスト.

        :param relative: テナントID以降の文字列
        :param json: リクエストボディ(jsonable object)
        """
        url = self.tenant_id_url(relative)
        return requests.post(
            url,
            headers=token_headers(),
            timeout=TIMEOUT * 3,  # VM addでタイムアウトしたから延長
            json=json,
        )

    def delete(self, relative: str) -> requests.Response:
        """HTTP DELETEリクエスト.

        :param relative: テナントID以降の文字列
        """
        url = self.tenant_id_url(relative)
        if self == Endpoints.IMAGE:
            url = self.url(relative)
        return requests.delete(
            url,
            headers=token_headers(),
            timeout=TIMEOUT * 3,
        )
