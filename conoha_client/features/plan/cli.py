"""VM Plan CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features import view_options

from .repo import first_vmplan_by, list_vmplans

if TYPE_CHECKING:
    from .domain import VMPlan


@click.group(name="plan")
def vm_plan_cli() -> None:
    """VM Plan CLI."""


@vm_plan_cli.command(name="ls")
@view_options
def _list() -> list[VMPlan]:
    return list_vmplans()


@vm_plan_cli.command(name="find")
@click.argument("attr_name")
@click.argument("value")
@view_options
def _find(attr_name: str, value: str) -> list[VMPlan]:
    return [first_vmplan_by(attr_name, value)]
