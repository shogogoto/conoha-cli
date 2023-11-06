"""VM Image CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features import view_options

from .repo import list_images

if TYPE_CHECKING:
    from .domain import Image


@click.command(name="lsimg", help="list image")
@view_options
def vm_image_cli() -> list[Image]:
    """VM Image CLI."""
    return list_images().root
