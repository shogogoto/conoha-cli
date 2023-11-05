"""template test."""


from pathlib import Path

import click
from _pytest.monkeypatch import MonkeyPatch
from click.testing import CliRunner

from conoha_client.features.template.domain import template_io

from .test_repo import OneModel


@click.command
@template_io
def cli() -> OneModel:
    """Testee cli."""
    return OneModel(x="xxx", extra="extra")


def test_template_read(monkeypatch: MonkeyPatch) -> None:
    """Test case."""
    p = Path(__file__).parent / "fixture_template.txt"
    monkeypatch.setenv("OS_TEMPLATE_READ", str(p))

    y = "aaaaaaaaaa"
    extra = "oooooooohhhhhhhhhh"
    runner = CliRunner()
    result = runner.invoke(cli, ["-m", "y", y, "-m", "extra", extra])
    assert "xxx" in result.stdout
    assert y in result.stdout
    assert extra not in result.stdout
