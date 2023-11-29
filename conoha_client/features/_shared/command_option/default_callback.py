from typing import Any, Callable, TypeAlias

import click

ClickCallback: TypeAlias = Callable[[click.Context, click.Parameter, Any], Any]


def default_callback(
    ctx: click.Context,  # noqa: ARG001
    param: click.Parameter,  # noqa: ARG001
    value: Any,  # noqa: ANN401
) -> Any:  # noqa: ANN401
    return value
