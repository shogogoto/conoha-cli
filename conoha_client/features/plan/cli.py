"""VM Plan CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features import view_options

from .repo import list_vmplans

if TYPE_CHECKING:
    from .domain import VMPlan


@click.group(name="plan")
def vm_plan_cli() -> None:
    """VM Plan CLI."""


@vm_plan_cli.command(name="ls")
@view_options
def _list() -> list[VMPlan]:
    return list_vmplans()
