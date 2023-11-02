"""template repository test."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from .repo import TemplateRepo


class OneModel(BaseModel, frozen=True):
    """a model for test."""

    x: str
    extra: str | None


def test_template() -> None:
    """Case."""
    p = Path(__file__).resolve().parent / "fixture_template.txt"
    x = "xxx.xxx.xxx.xxx"
    y = "/path/to/file"
    t = TemplateRepo(read_from=p, map_to={"y": y})
    one = OneModel(x=x, extra="extra")

    actual = t.apply(one)
    assert x in actual
    assert y in actual
