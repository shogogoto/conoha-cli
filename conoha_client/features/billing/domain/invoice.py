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
    tax_included: int = Field(alias="bill_plus_tax", description="税込み金額")
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
    """請求項目."""

    detail_id: int = Field(alias="invoice_detail_id")
    product_name: str = Field(alias="product_name")
    use_hours: int = Field(alias="quantity")
    unit_price: float = Field(alias="unit_price")
    started: datetime | None = Field(alias="start_date")

    @field_validator("started")
    def validate_used(cls, v: datetime) -> datetime | None:  # noqa: N805
        """Validate invoice datetime."""
        if v is not None:
            return v.astimezone(TOKYO_TZ)
        return None


class ConcatedInvoiceItem(BaseModel, frozen=True):
    """連結."""

    invoice_id: int
    detail_id: int
    product_name: str
    due: datetime
    # tax_included: int # 同じ請求の金額の重複表示が紛らわしい
    price: float = Field(alias="unit_price")
    use_hours: int
    # payment_method: str
    started: datetime | None


class InvoiceList(ModelList[Invoice], frozen=True):
    """invoice container."""

    def next_month_dues(self, now: datetime) -> InvoiceList:
        """来月の請求."""
        next_month = now + relativedelta(months=+1)
        ls = [e for e in self if e.due.month == next_month.month]
        return InvoiceList(root=ls)

    def filter_by_term(self, term: Term) -> InvoiceList:
        """支払い期日で絞る."""
        ls = [e for e in self if term.include(e.due)]
        return InvoiceList(root=ls)


class Term(BaseModel, frozen=True):
    """期間."""

    start: datetime
    end: datetime

    def include(self, dt: datetime) -> bool:
        """含まれるか."""
        return self.start <= dt < self.end

    @classmethod
    def create(cls, start: datetime, months: int) -> Term:
        """Create method."""
        end = start + relativedelta(months=months)
        return cls(start=start, end=end)


def first_day(dt: datetime | None = None) -> datetime:
    """今月."""
    if dt is None:
        dt = datetime.now(tz=TOKYO_TZ).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
    return dt + relativedelta(day=1)
