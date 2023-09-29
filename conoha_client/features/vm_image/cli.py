"""VM Image CLI."""
from __future__ import annotations

import click

from conoha_client.features._shared import view_options

from .repo import Image, find_id_by, list_images


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
    return find_id_by(attr_name, value)
