"""watch cli."""

import click


@click.command("watch", help="VM起動からn時間後に削除する")
@click.argument("vm_id", nargs=1, type=click.STRING)
def watch_cli() -> None:
    """Watch cli."""
