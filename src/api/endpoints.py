"""Conoha APIのサービス一覧."""
from __future__ import annotations

from enum import Enum
from urllib.parse import urljoin

import requests

from .environments import env_region, env_tenant_id
from .token import token_headers


class Endpoints(Enum):
    """Conoha APIのエンドポイントとバージョン情報のペア.

    ref: https://www.conoha.jp/docs/?btn_id=docs--sidebar_docs
    """

    ACCOUNT  = ("account",          "v1")
    COMPUTE  = ("compute",          "v2")
    VOLUME   = ("block.storage",    "v2")
    DATABASE = ("database-hosting", "v1")
    IMAGE    = ("image-service",    "v2")
    DNS      = ("dns-service",      "v1.0")
    STORAGE  = ("object-storage",   "v1")
    IDENTITY = ("identity",         "v2.0")
    NETWORK  = ("networking",       "v2.0")

    def __init__(self, prefix:str, version:str) -> None:
        """Enumのプロパティ設定."""
        self.prefix  = prefix
        self.version = version

    def url(self, relative:str)->str:
        """エンドポイントを組み立てる.

        :param relative: baseURL以降の文字列
        """
        p = self.prefix
        r = env_region()
        v = self.version
        base = f"https://{p}.{r}.conoha.io/{v}/"
        return urljoin(base, relative)

    def get(self, relative:str) -> requests.Response:
        """HTTPリクエストGETを呼ぶ.

        :param relative: テナントID以降の文字列
        """
        base = self.url(env_tenant_id()) + "/"
        url  = urljoin(base, relative)
        return requests.get(
            url,
            headers=token_headers(),
            timeout=3.0)
