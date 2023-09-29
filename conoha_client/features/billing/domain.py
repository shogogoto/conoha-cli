"""請求ドメイン."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Order(BaseModel, frozen=True):
    """一般請求情報."""

    order_id: str | None = Field(None, alias="uu_id")
    service_name: str
    start_at: datetime = Field(alias="service_start_date")
    status: str = Field(alias="item_status")

    def is_vps(self) -> bool:
        """order_idがUUID形式ならVPSの請求とみなす."""
        # try-catchでの判定はキモい
        try:
            UUID(self.order_id)
        except ValueError:
            return False
        except TypeError:
            return False
        else:
            return True


class VPSOrder(BaseModel, frozen=True):
    """VPS請求情報."""

    order_id: UUID = Field(alias="uu_id")
    product_name: str
    service_name: str
    billing_at: datetime = Field(alias="bill_start_date")
    unit_price: float
    status: str
