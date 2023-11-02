"""課金CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features._shared import view_options

from .repo import (
    VPSOrder,
    list_invoice_items,
    list_invoices,
    list_orders,
    list_payment,
    list_vps_orders,
)

if TYPE_CHECKING:
    from conoha_client.features.billing.domain import (
        ConcatedInvoiceItem,
        Deposit,
        Invoice,
        Order,
    )


@click.group(name="bill")
def billing_cli() -> None:
    """課金関連."""


@billing_cli.command(name="ls")
@view_options
def _list() -> list[VPSOrder]:
    """VPS請求一覧."""
    return list_vps_orders()


@billing_cli.command(name="ls-all")
@view_options
def _list_all() -> list[Order]:
    """請求一覧."""
    return list_orders()


@billing_cli.command(name="history")
@view_options
def _history() -> list[Deposit]:
    """入金履歴."""
    return list_payment()


@billing_cli.command(name="invoice")
@view_options
def _invoices() -> list[Invoice]:
    """課金一覧."""
    return list_invoices()


@billing_cli.command(name="invoice-items")
@view_options
def _invoices_items() -> list[ConcatedInvoiceItem]:
    """課金一覧."""
    return list_invoice_items()
