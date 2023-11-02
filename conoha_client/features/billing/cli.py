"""課金CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click
from dateutil.relativedelta import relativedelta

from conoha_client.features._shared import view_options
from conoha_client.features.billing.domain.invoice import Term, first_day

from .repo import (
    list_invoice_items,
    list_invoices,
    list_orders,
    list_payment,
    list_vps_orders,
)

if TYPE_CHECKING:
    from conoha_client.features.billing.domain import (
        Deposit,
    )


@click.group(name="bill")
def billing_cli() -> None:
    """課金関連."""


@billing_cli.command(name="order")
@click.option(
    "--vps/--all",
    is_flag=True,
    show_default=True,
    default=True,
    help="VPS契約のみ/全契約",
)
@view_options
def _list(vps: bool) -> list:
    """契約一覧."""
    if vps:
        return list_vps_orders()

    return list_orders().root


@billing_cli.command(name="paid")
@view_options
def _history() -> list[Deposit]:
    """入金履歴."""
    return list_payment()


@billing_cli.command(name="invoice")
@click.option(
    "--detail",
    "-d",
    is_flag=True,
    show_default=True,
    default=False,
)
@click.option(
    "--offset-monthly",
    "-o",
    "offset",
    type=click.INT,
    help="検索期間開始月のオフセット e.g. 1ヶ月前から=> -1",
    default=1,
    show_default=True,
)
@click.option(
    "--months",
    "-m",
    type=click.INT,
    help="検索月数",
    default=1,
    show_default=True,
)
@view_options
def _invoices(
    detail: bool,
    offset: int,
    months: int,
) -> list:
    """課金一覧."""
    start = first_day() + relativedelta(months=offset)
    term = Term.create(start, months)
    if detail:
        return list_invoice_items(term)

    return list_invoices().filter_by_term(term).root
