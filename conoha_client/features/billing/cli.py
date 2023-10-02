"""課金CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

import click

from conoha_client.features._shared import view_options

from .repo import VPSOrder, detail_order, list_orders

if TYPE_CHECKING:
    from conoha_client.features.billing.domain import Order


@click.group(name="bill")
def billing_cli() -> None:
    """課金関連."""


@billing_cli.command(name="ls")
@view_options
def _list() -> list[Order]:
    return list_orders()


@billing_cli.command()
@click.argument("vm_id")
@view_options
def find(vm_id: UUID) -> list[VPSOrder]:
    """VMのIDから請求情報を取得."""
    return [detail_order(vm_id)]
