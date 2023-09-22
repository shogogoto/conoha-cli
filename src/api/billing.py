"""請求情報照会."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from .endpoints import Endpoints
from .util import utc2jst

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class VPSOrder:
    """aaa."""

    order_id: UUID
    product_name: str
    service_name: str
    billing_at: datetime
    unit_price: int
    status: str

    @classmethod
    def parse(cls, one:dict) -> VPSOrder:
        """HTTPレスポンスから請求情報へ変換.

        :param one: json["order_items"]: list[dict]の要素
        """
        return VPSOrder(
            order_id = UUID(one["uu_id"]),
            product_name=one["product_name"],
            service_name=one["service_name"],
            billing_at=utc2jst(one["bill_start_date"]),
            unit_price=one["unit_price"],
            status=one["status"],
        )


# @cache
# def list_orders():
#     """サーバー設定一覧を取得する."""



#     for order in vps_orders:


def detail_order(order_id: str) -> VPSOrder:
    """サーバー設定一覧を取得する."""
    res = Endpoints.ACCOUNT.get(f"order-items/{order_id}").json()
    return VPSOrder.parse(res["order_item"])
