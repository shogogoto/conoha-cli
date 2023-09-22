"""サーバー設定情報."""
from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from uuid import UUID

from .endpoints import Endpoints


@dataclass(frozen=True)
class Flavor:
    """サーバー設定情報.

    :param flavor_id: フレーバーID
    :param memory_mb: RAMのメモリ容量(MB)
    :param n_core: CPUのコア数
    :param disk_gb: SSDブートディスク容量(GB)
    """

    flavor_id: UUID
    memory_mb: int
    n_core: int
    disk_gb: int

    @classmethod
    def parse(cls, one: dict)-> Flavor:
        """HTTPレスポンスからフレーバー情報へ変換.

        :param one: json["flavors"]: list[dict]の要素
        """
        return Flavor(
            flavor_id=UUID(one["id"]),
            memory_mb=int(one["ram"]),
            n_core=int(one["vcpus"]),
            disk_gb=int(one["disk"]),
        )


@cache
def list_flavors() -> list[Flavor]:
    """サーバー設定一覧を取得する."""
    res = Endpoints.COMPUTE.get("flavors/detail").json()
    return [Flavor.parse(e) for e in res["flavors"]]


def search_flavor(flavor_id: UUID) -> Flavor:
    """IDからフレーバーを返す.

    :param flavor_id: フレーバーID
    """
    def pred(e:Flavor) -> bool:
        return e.flavor_id == flavor_id

    result = filter(pred, list_flavors())
    return next(result)


