"""VM Action CLI option."""
from __future__ import annotations

from typing import Callable, Concatenate, ParamSpec, TextIO
from uuid import UUID

import click

from conoha_client.features.vm.repo.query import complete_vm_id

P = ParamSpec("P")
Param = Concatenate[tuple[str], TextIO, P]


def uuid_targets_options(
    func: Callable[Concatenate[UUID, ...], None],
) -> Callable[Param, None]:
    """標準入力からもuuidを取得できるオプション."""

    @click.argument("vm_ids", nargs=-1, type=click.STRING)
    @click.option(
        "--file",
        "-f",
        type=click.File("r"),
        default="-",
        help="対象のUUIDをファイル入力(default:標準入力)",
    )
    def wrapper(
        vm_ids: tuple[str],
        file: TextIO,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        uids = list(vm_ids)
        if not file.isatty():
            lines = file.read().splitlines()
            _uids = [UUID(line) for line in lines]
            uids.extend(_uids)

        for vm in [complete_vm_id(u) for u in uids]:
            func(vm.vm_id, *args, **kwargs)

    return wrapper
