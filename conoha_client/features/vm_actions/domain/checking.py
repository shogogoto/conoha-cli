"""check."""
from http import HTTPStatus
from uuid import UUID

from requests import Response

from .errors import VMSnapshotError


def check_snapshot(vm_id: UUID, res: Response) -> None:
    """Check snapshot response."""
    if res.status_code == HTTPStatus.CONFLICT:
        d = res.json().get("conflictingRequest")
        raise VMSnapshotError(d["message"])

    if res.status_code != HTTPStatus.ACCEPTED:
        rmsg = res.json()["message"]
        msg = f"{vm_id}をスナップショットできませんでした.{rmsg}"
        raise VMSnapshotError(msg)
