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


@click.command(name="lsorder")
@click.option(
    "--vps/--all",
    is_flag=True,
    show_default=True,
    default=True,
    help="VPS契約のみ/全契約",
)
@view_options
def order_cli(vps: bool) -> list:
    """契約一覧."""
    if vps:
        return list_vps_orders()

    return list_orders().root


@click.command(name="lspaid")
@view_options
def paid_cli() -> list[Deposit]:
    """入金履歴."""
    return list_payment()


@click.command(name="lsinvoice")
@click.option(
    "--detail",
    "-d",
    is_flag=True,
    show_default=True,
    default=False,
    help="請求項目詳細",
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
def invoice_cli(
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
