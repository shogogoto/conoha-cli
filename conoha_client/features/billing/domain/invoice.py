"""billing invoice dommain."""

from __future__ import annotations

from datetime import datetime

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, field_validator

from conoha_client.features._shared.model_list.domain import ModelList
from conoha_client.features._shared.util import TOKYO_TZ


class Invoice(BaseModel, frozen=True):
    """請求."""

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


class InvoiceList(ModelList[Invoice], frozen=True):
    """invoice container."""

    def next_month_dues(self, now: datetime) -> InvoiceList:
        """来月の請求."""
        next_month = now + relativedelta(months=+1)
        ls = [e for e in self if e.due.month == next_month.month]
        return InvoiceList(root=ls)


class InvoiceItem(BaseModel, frozen=True):
    """請求項目."""

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
