"""VM Plan Domain."""
from __future__ import annotations

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from conoha_client.features.plan.errors import FlavorIdentificationError


class VMPlan(BaseModel, frozen=True):
    """サーバー設定(VMプラン)情報."""

    flavor_id: UUID = Field(alias="id", description="フィレーバーID")
    name: str
    mem_mb: int = Field(alias="ram", description="RAMのメモリ容量(MB)")
    n_core: int = Field(alias="vcpus", description="CPUのコア数")
    disk_gb: int = Field(alias="disk", description="SSDブートディスク容量(GB)")

    @property
    def memory(self) -> Memory:
        """Get memory."""
        for m in Memory:
            if m.expression in self.name:
                return m
        raise FlavorIdentificationError


# 数字始まりの変数名にできなので単位をprefixにした
class Memory(str, Enum):
    """VMのメモリ容量."""

    MB512 = "0.5"
    GB1 = "1"
    GB2 = "2"
    GB4 = "4"
    GB8 = "8"
    GB16 = "16"
    GB32 = "32"
    GB64 = "64"

    @property
    def expression(self) -> str:
        """Flavor(VMプラン)を特定するための表現."""
        if self.is_smallest():
            return "m512d"
        return f"m{self.value}d"

    def is_smallest(self) -> bool:
        """最小のメモリか."""
        return self == Memory.MB512

    def is_match(self, img_name: str) -> bool:
        """valueがイメージ名に含まれているか."""
        if self.is_smallest():
            return "30gb" in img_name
        return "100gb" in img_name
