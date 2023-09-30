"""VM Plan Domain."""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class VMPlan(BaseModel, frozen=True):
    """サーバー設定(VMプラン)情報."""

    name: str
    flavor_id: UUID = Field(alias="id", description="フィレーバーID")
    mem_mb: int = Field(alias="ram", description="RAMのメモリ容量(MB)")
    n_core: int = Field(alias="vcpus", description="CPUのコア数")
    disk_gb: int = Field(alias="disk", description="SSDブートディスク容量(GB)")
