"""billing API."""
from __future__ import annotations

from http import HTTPStatus
from operator import attrgetter
from typing import Callable
from uuid import UUID

from conoha_client.features._shared import Endpoints

from .domain import (
    ConcatedInvoiceItem,
    Deposit,
    Invoice,
    InvoiceItem,
    Order,
    VPSOrder,
    is_uuid,
)


def list_orders() -> list[Order]:
    """請求一覧."""
    res = Endpoints.ACCOUNT.get("order-items").json()
    return [Order.model_validate(e) for e in res["order_items"]]


def detail_order(order_id: UUID) -> VPSOrder:
    """請求詳細を取得する."""
    res = Endpoints.ACCOUNT.get(f"order-items/{order_id}").json()
    return VPSOrder.model_validate(res["order_item"])


def list_vps_orders(
    list_dep: Callable[[], list[Order]] = list_orders,
    detail_dep: Callable[[UUID], VPSOrder] = detail_order,
) -> list[VPSOrder]:
    """VPS請求詳細一覧."""
    order_ids = {o.order_id for o in list_dep()}
    return [detail_dep(id_) for id_ in order_ids if is_uuid(id_)]


def list_payment() -> list[Deposit]:
    """入金履歴."""
    res = Endpoints.ACCOUNT.get("payment-history").json()
    return [Deposit.model_validate(e) for e in res["payment_history"]]


def list_invoices(
    offset: int = 0,
    limit: int = 1000,
) -> list[Invoice]:
    """課金一覧."""
    params = {
        "offset": offset,
        "limit": limit,
    }
    res = Endpoints.ACCOUNT.get("billing-invoices", params)
    return [Invoice.model_validate(e) for e in res.json()["billing_invoices"]]


def invoice_items(invoice_id: int) -> list[InvoiceItem]:
    """課金項目."""
    res = Endpoints.ACCOUNT.get(f"billing-invoices/{invoice_id}")
    if res.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        # 課金項目が存在しないっぽい
        return []
    items = res.json()["billing_invoice"]["items"]
    ls = [InvoiceItem.model_validate(e) for e in items]
    return sorted(ls, key=attrgetter("detail_id"))


def list_invoice_items() -> list[ConcatedInvoiceItem]:
    """課金項目一覧."""
    ls = list_invoices()
    _items = []
    for e in ls:
        items = invoice_items(e.invoice_id)
        _items.extend([e.concat(i) for i in items])
    return sorted(_items, key=attrgetter("detail_id"))
