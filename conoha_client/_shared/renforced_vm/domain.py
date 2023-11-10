"""reinforced VM domain."""
from __future__ import annotations

from datetime import timedelta
from ipaddress import IPv4Address
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from conoha_client.features.vm.domain import VMStatus  # noqa: TCH001


class ReinforcedVM(BaseModel, frozen=True):
    """human friendly VM, not just API Return."""

    ipv4: IPv4Address
    status: VMStatus
    elapsed: timedelta
    image_name: str
    memoryMB: int = Field(alias="mem_mb")  # noqa: N815
    n_cpu: int = Field(alias="n_core")
    storageGB: int = Field(alias="disk_gb")  # noqa: N815
    sshkey: str | None
    vm_id: UUID

    @field_serializer("elapsed")
    def _serialize(self, v: timedelta) -> str:
        """表示を整える."""
        return str(v)
