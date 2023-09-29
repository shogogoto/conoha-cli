from __future__ import annotations

import json
from uuid import UUID, uuid4

import click
import pytest
from click.testing import CliRunner
from pydantic import BaseModel

from .domain import ExtraKeyError, model_filter, view_options


class TestModel(BaseModel):
    """for test."""

    x: str
    y: UUID


def test_model_filter() -> None:
    """Valid test."""
    m = TestModel(x="x", y=uuid4())
    assert model_filter(m, {"x"}) == {"x": "x"}
    assert model_filter(m, {"y"}) == {"y": str(m.y)}
    assert model_filter(m) == {"x": "x", "y": str(m.y)}


def test_invalid_model_filter() -> None:
    """Invalid test."""
    m = TestModel(x="x", y=uuid4())
    with pytest.raises(ExtraKeyError):
        model_filter(m, {"extra"})
    with pytest.raises(ExtraKeyError):
        model_filter(m, {"x", "extra"})


t1 = TestModel(x="name1", y=uuid4())
t2 = TestModel(x="name2", y=uuid4())
t3 = TestModel(x="name3", y=uuid4())
tm = [t1, t2, t3]


@click.command()
@view_options
def cli() -> list[TestModel]:
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
