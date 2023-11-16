"""watch cli."""

import click

from conoha_client.features.vm.repo.query import complete_vm
from conoha_client.features.vm_actions.repo import remove_vm

from .repo import (
    broadcast_message,
    elapsed_from_created,
    saved_vm,
    stopped_vm,
    wait_plus_charge,
)


@click.command("rm-gracefully", help="追加課金される前にVMを保存・削除する")
@click.argument("vm_id", nargs=1, type=click.STRING)
@click.argument("save_name", nargs=1, type=click.STRING)
@click.option(
    "--buffer-min",
    "-b",
    type=click.INT,
    default=5,
    show_default=True,
    help="追加課金される前に削除完了するための猶予[min]",
)
@click.option(
    "--hours",
    "-h",
    type=click.FLOAT,
    default=1.0,
    show_default=True,
    help="追加課金が発生する時間[h]",
)
def graceful_rm_cli(
    vm_id: str,
    save_name: str,
    buffer_min: int,
    hours: float,
) -> None:
    """Watch cli."""
    id_ = complete_vm(vm_id).vm_id
    deadline_min = int(hours * 60)
    try:
        wait_plus_charge(
            id_,
            buffer_min,
            deadline_min - 2,
        )
        bmsg = (
            f"VM({id_}) makes additional charge "
            f"when it takes {deadline_min} minutes. "
            f"So this VM will be saved and removed after 2 minutes."
        )
        broadcast_message(bmsg)

        wait_plus_charge(
            id_,
            buffer_min,
            deadline_min,
        )
        msg = "VM is going to be saved and removed right now."
        broadcast_message(msg)

        elp_stop = stopped_vm(id_)
        click.echo(f"It took {elp_stop} to stop VM({id_})")

        elp_sv = saved_vm(id_, save_name)
        click.echo(f"It took {elp_sv} to save VM({id_})")

        # たまにremoved VMが取得できない場合があるので
        # 数秒不正確でも削除直前の経過時間を表示する
        elapsed = elapsed_from_created(id_)()
        remove_vm(id_)
        click.echo(f"VM({id_}) was removed")
        click.echo(f"Duration time of VM({id_}) was {elapsed}")
    except Exception:  # noqa: BLE001
        errmsg = f"failed to remove VM({id_}) gracefully."
        broadcast_message(errmsg)
