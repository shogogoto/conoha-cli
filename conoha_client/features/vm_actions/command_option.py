"""VM Action CLI option."""
from __future__ import annotations

import functools
from typing import Callable, Concatenate, ParamSpec, TextIO, TypeAlias, TypeVar
from uuid import UUID

import click
from pydantic import BaseModel

from conoha_client.features.vm.repo.query import complete_vm

P = ParamSpec("P")
Wrapped: TypeAlias = Callable[Concatenate[UUID, P], None]
Param: TypeAlias = Concatenate[tuple[str], TextIO, P]
Return: TypeAlias = Callable[Param, None]
Complete: TypeAlias = Callable[[str], UUID]
T = TypeVar("T", bound=BaseModel)


def default_complete(pre_uuid: str) -> UUID:
    """Complete uuid as default."""
    return complete_vm(pre_uuid).vm_id


class Wrapper(BaseModel, frozen=True):
    """wrap command."""

    dep: Complete

    def __call__(self, func: Wrapped) -> Return:
        """標準入力からもuuidを取得できるオプション."""

        @click.argument("vm_ids", nargs=-1, type=click.STRING)
        @click.option(
            "--file",
            "-f",
            type=click.File("r"),
            default="-",
            help="対象のUUIDをファイル入力(default:標準入力)",
        )
        @functools.wraps(func)
        def wrapper(
            vm_ids: tuple[str],
            file: TextIO,
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> None:
            uuids = list(vm_ids)
            if not file.isatty():
                lines = file.read().splitlines()
                uuids.extend(lines)

            completed = [self.dep(u) for u in uuids]
            for uid in completed:
                func(uid, *args, **kwargs)

        return wrapper


def uuid_complete_options(
    complete: Complete = default_complete,
) -> Callable[[Wrapped], Return]:
    """Decorate with uuid completion."""
    return Wrapper(dep=complete)
