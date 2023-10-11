"""VM Actions CLI test."""

from uuid import UUID, uuid4

import click
from click.testing import CliRunner

from conoha_client.features.vm_actions.command_option import uuid_targets_options


@click.command()
@uuid_targets_options
def cli(uid: UUID) -> None:
    """Testee cli."""
    click.echo(f"{uid} was input")


@click.command()
@click.option("--option", "-o")
@uuid_targets_options
def cli_with_other_options(uid: UUID, option: str) -> None:
    """Testee cli2."""
    click.echo(f"{uid} and {option}")


def test_uuid_target_option() -> None:
    """uuid_target_optionsデコレータのテスト."""
    runner = CliRunner()
    uid = str(uuid4())
    result = runner.invoke(cli, [str(uid)])
    assert uid in result.stdout


def test_with_other_option() -> None:
    """Another case."""
    runner = CliRunner()
    uid = str(uuid4())
    result = runner.invoke(
        cli_with_other_options,
        [str(uid), "-o", "opt"],
    )
    assert uid in result.stdout
    assert "opt" in result.stdout
