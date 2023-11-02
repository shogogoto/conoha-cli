"""請求ドメイン."""
from __future__ import annotations

from datetime import datetime
from typing import Any, TypeGuard
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

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
    """一般請求情報."""

    order_id: UUID | int | None = Field(None, alias="uu_id")
    service_name: str
    status: str = Field(alias="item_status")
    started: datetime = Field(alias="service_start_date")

    @field_validator("started")
    def validate(cls, v: datetime) -> datetime:  # noqa: N805
        """Validate start at."""
        return v.astimezone(TOKYO_TZ)

    def is_vps(self) -> bool:
        """order_idがUUID形式ならVPSの請求とみなす."""
        return is_uuid(self.order_id)


class VPSOrder(BaseModel, frozen=True):
    """VPS請求情報."""

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


class Deposit(BaseModel, frozen=True):
    """入金."""

    amount: int = Field(alias="deposit_amount")
    money_type: str = Field(alias="money_type")
    received: datetime = Field(alias="received_date")

    @field_validator("received")
    def validate(cls, v: datetime) -> datetime:  # noqa: N805
        """Validate datetime."""
        return v.astimezone(TOKYO_TZ)


class Invoice(BaseModel, frozen=True):
    """課金."""

    invoice_id: int = Field(alias="invoice_id")
    tax_included: int = Field(alias="bill_plus_tax")
    payment_method: str = Field(alias="payment_method_type")
    occurred: datetime = Field(alias="invoice_date")
    due: datetime = Field(alias="due_date")

    @field_validator("due")
    def validate_due(cls, v: datetime) -> datetime:  # noqa: N805
        """Validate due datetime."""
        return v.astimezone(TOKYO_TZ)

    @field_validator("occurred")
    def validate_invoiced(cls, v: datetime) -> datetime:  # noqa: N805
        """Validate invoice datetime."""
        return v.astimezone(TOKYO_TZ)

    def concat(self, item: InvoiceItem) -> ConcatedInvoiceItem:
        """Concatenate."""
        d = self.model_dump(mode="json") | item.model_dump(mode="json")
        return ConcatedInvoiceItem.model_validate(d)


class InvoiceItem(BaseModel, frozen=True):
    """課金項目."""

    detail_id: int = Field(alias="invoice_detail_id")
    product_name: str = Field(alias="product_name")
    quantity: int = Field(alias="quantity")
    started: datetime | None = Field(alias="start_date")
    unit_price: float = Field(alias="unit_price")


class ConcatedInvoiceItem(BaseModel, frozen=True):
    """連結."""

    # invoice_id: int
    due: datetime
    detail_id: int
    product_name: str
    price: float = Field(alias="unit_price")

    quantity: int
    tax_included: int
    # payment_method: str
    started: datetime | None
