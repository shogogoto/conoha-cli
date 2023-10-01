from __future__ import annotations

import json
from uuid import UUID, uuid4

import click
import pytest
from click.testing import CliRunner
from pydantic import AliasPath, BaseModel, Field

from .domain import ExtraKeyError, model_filter, view_options


class ExampleModel(BaseModel):
    """for test."""

    x: str
    y: UUID
    dist: str = Field("", alias=AliasPath("metadata", "dst"))


def test_model_filter() -> None:
    """Valid test."""
    m = ExampleModel(x="x", y=uuid4())
    assert model_filter(m, {"x"}) == {"x": "x"}
    assert model_filter(m, {"y"}) == {"y": str(m.y)}
    assert model_filter(m) == {"x": "x", "y": str(m.y), "dist": ""}


def test_invalid_model_filter() -> None:
    """Invalid test."""
    m = ExampleModel(x="x", y=uuid4())
    with pytest.raises(ExtraKeyError):
        model_filter(m, {"extra"})
    with pytest.raises(ExtraKeyError):
        model_filter(m, {"x", "extra"})


t1 = ExampleModel(x="name1", y=uuid4())
t2 = ExampleModel(x="name2", y=uuid4())
t3 = ExampleModel(x="name3", y=uuid4())
tm = [t1, t2, t3]


@click.command()
@view_options
def cli() -> list[ExampleModel]:
    return tm


def test_view_option_json() -> None:
    """Json view test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["-s", "json"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == [t.model_dump(mode="json") for t in tm]


def test_view_option_table() -> None:
    """Table view test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["x", "-s", "table", "-p"])
    assert result.exit_code == 0
    assert result.stdout.split() == [t.x for t in tm]
