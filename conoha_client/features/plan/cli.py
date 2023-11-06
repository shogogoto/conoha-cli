"""VM Plan CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features import view_options

from .repo import list_vmplans

if TYPE_CHECKING:
    from .domain import VMPlan


@click.command(name="lsplan")
@view_options
def vm_plan_cli() -> list[VMPlan]:
    """List vm plan."""
    return list_vmplans()
