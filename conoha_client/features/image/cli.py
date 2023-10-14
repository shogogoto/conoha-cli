"""VM Image CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features import view_options

from .repo import list_images

if TYPE_CHECKING:
    from .domain import Image


@click.group(name="image")
def vm_image_cli() -> None:
    """VM Image CLI."""


@vm_image_cli.command(name="ls")
@view_options
def _list() -> list[Image]:
    return list_images()
