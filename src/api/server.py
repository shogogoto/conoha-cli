"""契約中サーバー情報."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
from uuid import UUID

import requests
from dateutil import parser
from pytz import timezone

from .endpoints import Endpoints
from .environments import env_tenant_id
from .flavor import Flavor, search_flavor
from .token import token_headers


class Status(Enum):
    """契約中Serverの状態."""

    ACTIVE  = auto()
    SHUTOFF = auto()
    REBOOT  = auto()

    def is_shutoff(self) -> bool:
        """シャットダウン済みか否か."""
        return self == Status.SHUTOFF


@dataclass(frozen=True)
class Server:
    r"""契約中のサーバー.

    :param ipv4: 固定IPアドレス
    :param created_at: 作成日時(JST)
    :param updated_at: 更新日時(JST)
    :param status: \[ACTIVE|SHUTOFF|REBOOT\]
    :param image_id: イメージID
    :param flavor: コア数などの設定情報
    """

    ipv4: str
    created_at: datetime
    updated_at: datetime
    status: Status
    image_id: UUID
    flavor: Flavor

    def elapsed_from_created(self) -> timedelta:
        """作成時からの経過時間を秒以下を省いて計算する."""
        tz = timezone("Asia/Tokyo")
        n = datetime.now(tz).replace(second=0, microsecond=0)
        return n - self.created_at

    @classmethod
    def parse(cls, one: dict)-> Server:
        """HTTPレスポンスからサーバー情報へ変換.

        :param one: json["servers"]: list[dict]の要素
        """
        flavor_id = UUID(one["flavor"]["id"])
        return Server(
            ipv4 = one["name"].replace("-", "."),
            status = Status[one["status"]],
            created_at = utc2jst(one["created"]),
            updated_at = utc2jst(one["updated"]),
            image_id = UUID(one["image"]["id"]),
            flavor = search_flavor(flavor_id),
        )


def utc2jst(utc_str: str) -> datetime:
    """UTC文字列をJST Datetimeへ変換."""
    tz = timezone("Asia/Tokyo")
    return parser.parse(utc_str) \
            .astimezone(tz)


def list_servers() -> list[Server]:
    """契約中のサーバー情報一覧を取得する."""
    tid = env_tenant_id()
    url = Endpoints.COMPUTE.url(f"{tid}/servers/detail")
    res = requests.get(url, headers=token_headers(), timeout=3.0) \
            .json()
    return [Server.parse(e) for e in res["servers"]]
