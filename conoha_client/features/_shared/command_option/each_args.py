from __future__ import annotations

import functools
from typing import Callable, Concatenate, Generic, ParamSpec, TextIO, TypeAlias, TypeVar

import click
from pydantic import BaseModel

P = ParamSpec("P")
T = TypeVar("T")
Wrapped: TypeAlias = Callable[Concatenate[T, P], None]
Param: TypeAlias = Concatenate[tuple[str], TextIO, P]
Return: TypeAlias = Callable[Param, None]
Converter: TypeAlias = Callable[[str], T]


class Wrapper(BaseModel, Generic[T], frozen=True):
    """wrap command."""

    root: Converter[T]
    arg_name: str

    def __call__(self, func: Wrapped) -> Return:
        """標準入力からもuuidを取得できるオプション."""

        @click.argument(self.arg_name, nargs=-1, type=click.STRING)
        @click.option(
            "--file",
            "-f",
            type=click.File("r"),
            default="-",
            help="対象のUUIDをファイル入力(default:標準入力)",
        )
        @functools.wraps(func)
        def wrapper(
            params: tuple[str],
            file: TextIO,
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> None:
            _params = list(params)
            if not file.isatty():
                lines = file.read().splitlines()
                _params.extend(lines)

            completed = [self.root(p) for p in _params]
            for uid in completed:
                func(uid, *args, **kwargs)

        return wrapper


def each_args(
    arg_name: str = "params",
    converter: Converter = lambda x: x,
) -> Callable[[Wrapped], Return]:
    """Decorate with uuid completion."""
    return Wrapper(root=converter, arg_name=arg_name)
