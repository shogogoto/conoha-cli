"""VM Plan CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features._shared import view_options

from .repo import find_id_by, list_flavors

if TYPE_CHECKING:
    from .domain import Flavor


@click.group(name="plan")
def vm_plan_cli() -> None:
    """VM Plan CLI."""


@vm_plan_cli.command(name="ls")
@view_options
def _list() -> list[Flavor]:
    return list_flavors()


@vm_plan_cli.command(name="find")
@click.argument("attr_name")
@click.argument("value")
@view_options
def _find(attr_name: str, value: str) -> list[Flavor]:
    return find_id_by(attr_name, value)
