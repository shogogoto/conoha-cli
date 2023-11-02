"""billing order domain."""

from __future__ import annotations

from datetime import datetime
from typing import Any, TypeGuard
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from conoha_client.features._shared.model_list.domain import ModelList
from conoha_client.features._shared.util import TOKYO_TZ


def is_uuid(v: Any) -> TypeGuard[UUID]:  # noqa: ANN401
    """Is uuid."""
    # try-catchでの判定はキモい
    try:
        UUID(str(v))
    except ValueError:
        return False
    except TypeError:
        return False
    except AttributeError:
        return False
    else:
        return True


class Order(BaseModel, frozen=True):
    """契約."""

    order_id: UUID | int | None = Field(None, alias="uu_id")
    service_name: str
    status: str = Field(alias="item_status")
    started: datetime = Field(alias="service_start_date")

    @field_validator("started")
    def validate(cls, v: datetime) -> datetime:  # noqa: N805
        """Validate start at."""
        return v.astimezone(TOKYO_TZ)


class DetailOrder(BaseModel, frozen=True):
    """契約詳細."""

    vm_id: UUID = Field(alias="uu_id", description="order_idと同一")
    product_name: str
    service_name: str
    unit_price: float
    status: str
    started: datetime = Field(alias="bill_start_date")

    @field_validator("started")
    def validate(cls, v: datetime) -> datetime:  # noqa: N805
        """Validate start at."""
        return v.astimezone(TOKYO_TZ)


class OrderList(ModelList[Order], frozen=True):
    """契約一覧."""

    def filter_vps(self) -> OrderList:
        """VPS契約を抽出."""
        return OrderList(root=[o for o in self if is_uuid(o.order_id)])
