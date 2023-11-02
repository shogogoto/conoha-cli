from __future__ import annotations

import json
from uuid import UUID, uuid4

import click
import pytest
from click.testing import CliRunner
from pydantic import AliasPath, BaseModel, Field

from .domain import ExtraKeyError, model_extract, model_filter, view_options


class ExampleModel(BaseModel):
    """for test."""

    x: str
    y: UUID
    dist: str = Field("", alias=AliasPath("metadata", "dst"))


def test_model_extract() -> None:
    """Valid test."""
    m = ExampleModel(x="x", y=uuid4())
    assert model_extract(m, {"x"}) == {"x": "x"}
    assert model_extract(m, {"y"}) == {"y": str(m.y)}
    assert model_extract(m) == {"x": "x", "y": str(m.y), "dist": ""}


def test_invalid_model_filter() -> None:
    """Invalid test."""
    m = ExampleModel(x="x", y=uuid4())
    with pytest.raises(ExtraKeyError):
        model_extract(m, {"extra"})
    with pytest.raises(ExtraKeyError):
        model_extract(m, {"x", "extra"})


t1 = ExampleModel(x="name1", y=uuid4())
t2 = ExampleModel(x="name2", y=uuid4())
t3 = ExampleModel(x="name3", y=uuid4())
tm = [t1, t2, t3]


def test_model_filter() -> None:
    """モデルをフィルターする."""
    assert [t1] == model_filter(tm, key="x", value="1")
    with pytest.raises(ExtraKeyError):
        model_filter(tm, key="unknown", value="1")


@click.command()
@view_options
def cli() -> list[ExampleModel]:
    return tm


def test_view_option_json() -> None:
    """Json view test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--json"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == [t.model_dump(mode="json") for t in tm]


def test_view_option_table() -> None:
    """Table view test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["-k", "x", "--table", "-p"])
    assert result.exit_code == 0
    assert result.stdout.split() == [t.x for t in tm]


def test_view_filter_option() -> None:
    """Table view test."""
    runner = CliRunner()
    result = runner.invoke(cli, ["-k", "x", "--where", "x", "1", "-p"])
    assert result.exit_code == 0
    assert result.stdout.split() == [t1.x]
