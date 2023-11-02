"""billing API."""
from __future__ import annotations

from http import HTTPStatus
from operator import attrgetter
from typing import Callable
from uuid import UUID

from conoha_client.features._shared import Endpoints
from conoha_client.features.billing.domain.invoice import InvoiceList, Term

from .domain import (
    ConcatedInvoiceItem,
    Deposit,
    DetailOrder,
    Invoice,
    InvoiceItem,
    Order,
    OrderList,
)


def list_orders() -> OrderList:
    """契約一覧."""
    res = Endpoints.ACCOUNT.get("order-items").json()
    ls = [Order.model_validate(e) for e in res["order_items"]]
    return OrderList(root=ls)


def detail_order(order_id: UUID) -> DetailOrder:
    """契約詳細を取得する."""
    res = Endpoints.ACCOUNT.get(f"order-items/{order_id}").json()
    return DetailOrder.model_validate(res["order_item"])


def list_vps_orders(
    list_dep: Callable[[], OrderList] = list_orders,
    detail_dep: Callable[[UUID], DetailOrder] = detail_order,
) -> list[DetailOrder]:
    """VPS契約詳細一覧."""
    ids = {o.order_id for o in list_dep().filter_vps()}
    return [detail_dep(uid) for uid in ids]


def list_payment() -> list[Deposit]:
    """入金履歴."""
    res = Endpoints.ACCOUNT.get("payment-history").json()
    return [Deposit.model_validate(e) for e in res["payment_history"]]


def dep_invoice_json(offset: int, limit: int) -> list[object]:
    """Invoice request dependency."""
    params = {
        "offset": offset,
        "limit": limit,
    }
    res = Endpoints.ACCOUNT.get("billing-invoices", params)
    return res.json()["billing_invoices"]


def list_invoices(
    offset: int = 0,
    limit: int = 1000,
    dep: Callable[[int, int], list[object]] = dep_invoice_json,
) -> InvoiceList:
    """課金一覧."""
    ls = [Invoice.model_validate(e) for e in dep(offset, limit)]
    return InvoiceList(root=ls)


def invoice_items(invoice_id: int) -> list[InvoiceItem]:
    """課金項目."""
    res = Endpoints.ACCOUNT.get(f"billing-invoices/{invoice_id}")
    if res.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        # 課金項目が存在しないっぽい
        return []
    items = res.json()["billing_invoice"]["items"]
    ls = [InvoiceItem.model_validate(e) for e in items]
    return sorted(ls, key=attrgetter("detail_id"))


def list_invoice_items(term: Term | None = None) -> list[ConcatedInvoiceItem]:
    """課金項目一覧."""
    ls = list_invoices()
    if term is not None:
        ls = ls.filter_by_term(term)
    _items = []
    for e in ls:
        items = invoice_items(e.invoice_id)
        _items.extend([e.concat(i) for i in items])
    return sorted(_items, key=attrgetter("detail_id"))
