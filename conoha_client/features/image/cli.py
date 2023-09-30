"""VM Image CLI."""
from __future__ import annotations

from typing import TYPE_CHECKING

import click

from conoha_client.features import view_options

from .repo import find_image_by, list_images

if TYPE_CHECKING:
    from .domain import Image


@click.group(name="image")
def vm_image_cli() -> None:
    """VM Image CLI."""


@vm_image_cli.command(name="ls")
@view_options
def _list() -> list[Image]:
    return list_images()


@vm_image_cli.command(name="find")
@click.argument("attr_name")
@click.argument("value")
@view_options
def _find(attr_name: str, value: str) -> list[Image]:
    img = find_image_by(attr_name, value)
    if img is None:
        return []
    return [img]
